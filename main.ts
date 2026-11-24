// bring-the-humans-03 — entry program, written for this entry.
//
// What it does, in one sentence: hand the grader the address of the
// TikTok video that is this entry, by placing our VIDEO.json into the
// output folder the grader reads.
//
// The video itself lives on TikTok (posted publicly from @alshop_234);
// this file never touches the video bytes. It only moves the small JSON
// pointer file, and it refuses to move a pointer that does not look
// like a real TikTok video address, so a typo fails loudly here instead
// of silently at grading time.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const VIDEO_FILE = "VIDEO.json";

function folderFromEnv(name: string, fallback: string): string {
  const seen = process.env[name];
  return seen !== undefined && seen.length > 0 ? seen : fallback;
}

function fail(message: string): never {
  console.error(`bring-the-humans-03: ${message}`);
  process.exit(1);
}

const sourceFolder = folderFromEnv("MAKEFUN_BOT_DIR", "/bot");
const targetFolder = folderFromEnv("MAKEFUN_OUTPUT_DIR", "/output");
const sourcePath = resolve(sourceFolder, VIDEO_FILE);
const targetPath = resolve(targetFolder, VIDEO_FILE);

if (!existsSync(sourcePath)) {
  fail(`no ${VIDEO_FILE} found in ${sourceFolder}; nothing to hand to the grader.`);
}

const rawText = readFileSync(sourcePath, "utf8");

let parsed: unknown;
try {
  parsed = JSON.parse(rawText);
} catch {
  fail(`${VIDEO_FILE} in ${sourceFolder} is not valid JSON.`);
}

const entry = parsed as { url?: unknown };
if (typeof entry.url !== "string" || !entry.url.startsWith("https://www.tiktok.com/")) {
  fail(`${VIDEO_FILE} does not name a TikTok video address (expected https://www.tiktok.com/...).`);
}

mkdirSync(targetFolder, { recursive: true });
writeFileSync(targetPath, rawText, "utf8");
console.log(`bring-the-humans-03: handed ${entry.url} to the grader at ${targetPath}.`);
