#!/usr/bin/env node
/**
 * Fact-checker for opedal.tech
 * 
 * Validates numeric claims in src/ against content/facts.yml and cv/data/architect.yml.
 * 
 * Usage:
 *   node scripts/check-facts.mjs
 * 
 * Exit codes:
 *   0 — all claims verified
 *   1 — one or more claims failed verification
 */

import { readFileSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';
import yaml from 'js-yaml';

const REPO_ROOT = resolve(new URL('.', import.meta.url).pathname.replace(/^\/([A-Z]:)/, '$1'), '..');
const FACTS_PATH = join(REPO_ROOT, 'content', 'facts.yml');
const ARCHITECT_PATH = join(REPO_ROOT, 'cv', 'data', 'architect.yml');
const SRC_DIR = join(REPO_ROOT, 'src');

// Exclusion list: file-relative line numbers or patterns to skip
// Format: { "path/to/file.astro": [lineNumber, ...] } or regex patterns
const EXCLUSIONS = {
  // Exclude CSS numeric values, years in blog post pubDate, and other non-fact numbers
  patterns: [
    /\d{4}-\d{2}-\d{2}/, // ISO dates (pubDate in frontmatter)
    /\b(width|height|padding|margin|font-size|gap|max-width|min-width|line-height|z-index|opacity|transition|duration):\s*\d+/i,
    /\bpubDate:\s*\d{4}-/i, // Frontmatter pubDate
    /node-version:\s*['"]?\d+['"]?/i, // Node version in workflow files
  ],
};

function loadYaml(path) {
  try {
    return yaml.load(readFileSync(path, 'utf8'));
  } catch (err) {
    console.error(`❌ Failed to load ${path}:`, err.message);
    process.exit(1);
  }
}

function walkDir(dir, extensions, results = []) {
  const entries = readdirSync(dir);
  for (const entry of entries) {
    const fullPath = join(dir, entry);
    const stat = statSync(fullPath);
    if (stat.isDirectory()) {
      walkDir(fullPath, extensions, results);
    } else if (extensions.some(ext => entry.endsWith(ext))) {
      results.push(fullPath);
    }
  }
  return results;
}

function shouldExcludeLine(line) {
  return EXCLUSIONS.patterns.some(pattern => pattern.test(line));
}

function checkFile(filePath, derivedFacts) {
  const content = readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  const errors = [];

  // Word-to-number mapping
  const wordToNum = {
    one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10,
    eleven: 11, twelve: 12, thirteen: 13, fourteen: 14, fifteen: 15, sixteen: 16, seventeen: 17,
    eighteen: 18, nineteen: 19, twenty: 20, thirty: 30, forty: 40, fifty: 50,
  };

  lines.forEach((line, idx) => {
    const lineNumber = idx + 1;
    
    // Skip excluded lines
    if (shouldExcludeLine(line)) return;

    // Pattern 1: "N years" or "N+ years" or "word years" — numeric tenure claims
    const tenureMatches = line.matchAll(/(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|twenty|thirty|forty|fifty)\+?\s*years?/gi);
    for (const match of tenureMatches) {
      const matchText = match[1].toLowerCase();
      const claimedYears = wordToNum[matchText] || parseInt(match[1], 10);
      const validValues = Object.values(derivedFacts).filter(v => typeof v === 'number');
      
      if (!validValues.includes(claimedYears)) {
        errors.push({
          line: lineNumber,
          text: line.trim(),
          claim: `${match[1]} years`,
          expected: validValues,
        });
      }
    }

    // Pattern 2: "N years at EMPLOYER" — cross-check against YAML
    const employerMatches = line.matchAll(/(\d+)\s+years?\s+(?:at|with)\s+(\w+)/gi);
    for (const match of employerMatches) {
      const claimedYears = parseInt(match[1], 10);
      const employer = match[2].toLowerCase();
      
      if (employer === 'microsoft' && claimedYears !== derivedFacts.years_at_microsoft) {
        errors.push({
          line: lineNumber,
          text: line.trim(),
          claim: `${claimedYears} years at Microsoft`,
          expected: [derivedFacts.years_at_microsoft],
        });
      }
    }

    // Pattern 3: "co-founded N breweries" or "founded N companies"
    const ventureMatches = line.matchAll(/(co[- ]?founded?|founded)\s+(\w+)\s+(brewer\w+|companies)/gi);
    for (const match of ventureMatches) {
      const countMatch = line.match(/\b(two|three|four|five|\d+)\b/i);
      if (countMatch) {
        const claimedCount = wordToNum[countMatch[1].toLowerCase()] || parseInt(countMatch[1], 10);
        
        if (claimedCount !== derivedFacts.breweries_cofounded) {
          errors.push({
            line: lineNumber,
            text: line.trim(),
            claim: `co-founded ${claimedCount} breweries`,
            expected: [derivedFacts.breweries_cofounded],
          });
        }
      }
    }

    // Pattern 4: Brewery names — must be in the approved list
    const breweryNamePattern = /\b(cervisiam|krecher)\b/gi;
    const breweryMatches = line.matchAll(breweryNamePattern);
    for (const match of breweryMatches) {
      const nameFound = match[1].toLowerCase();
      const validNames = derivedFacts.brewery_names.map(n => n.toLowerCase());
      if (!validNames.includes(nameFound)) {
        errors.push({
          line: lineNumber,
          text: line.trim(),
          claim: `brewery name "${match[1]}"`,
          expected: derivedFacts.brewery_names,
        });
      }
    }

    // Pattern 5: Cervisiam + exit claims — FAIL if "sold" or "exited" near Cervisiam (still active)
    // Must check that the exit verb applies to Cervisiam, not to Krecher in the same sentence
    const cervisiamExitPattern = /cervisiam\s+(is|was)?\s*(sold|exited|closed|ended)/i;
    if (cervisiamExitPattern.test(line)) {
      errors.push({
        line: lineNumber,
        text: line.trim(),
        claim: 'Cervisiam sold/exited/ended claim',
        expected: ['Cervisiam is still active per facts.yml'],
      });
    }

    // Pattern 6: Krecher end year — if krecher_end_year is set, verify any year mention
    if (derivedFacts.krecher_end_year && /krecher/i.test(line)) {
      const yearMatch = line.match(/\b(20\d{2})\b/);
      if (yearMatch) {
        const claimedYear = parseInt(yearMatch[1], 10);
        if (claimedYear !== derivedFacts.krecher_end_year) {
          errors.push({
            line: lineNumber,
            text: line.trim(),
            claim: `Krecher end year ${claimedYear}`,
            expected: [derivedFacts.krecher_end_year],
          });
        }
      }
    }
  });

  return errors;
}

function main() {
  console.log('🔍 Fact-checking opedal.tech content...\n');

  // Load facts
  const facts = loadYaml(FACTS_PATH);
  const architect = loadYaml(ARCHITECT_PATH);

  // Compute derived facts
  const currentYear = new Date().getFullYear();
  const derivedFacts = {
    years_with_azure_entra_m365: currentYear - facts.career.azure_first_used_year,
    years_at_microsoft: currentYear - facts.career.microsoft_start_year,
    years_at_teknograd: 2020 - facts.career.teknograd_start_year, // 2011–2020 from architect.yml
    breweries_cofounded: facts.ventures.breweries_cofounded,
    brewery_names: facts.ventures.brewery_names || [],
    bar_names: facts.ventures.bar_names || [],
    cervisiam_status: facts.ventures.cervisiam_status,
    krecher_status: facts.ventures.krecher_status,
    krecher_end_year: facts.ventures.krecher_end_year || null,
  };

  console.log('📊 Derived facts:');
  console.log(`   - Years with Azure/M365/Entra: ${derivedFacts.years_with_azure_entra_m365}`);
  console.log(`   - Years at Microsoft: ${derivedFacts.years_at_microsoft}`);
  console.log(`   - Years at Teknograd: ${derivedFacts.years_at_teknograd}`);
  console.log(`   - Breweries co-founded: ${derivedFacts.breweries_cofounded}`);
  console.log(`   - Brewery names: ${derivedFacts.brewery_names.join(', ')}`);
  console.log(`   - Bar names: ${derivedFacts.bar_names.join(', ')}`);
  console.log(`   - Cervisiam status: ${derivedFacts.cervisiam_status}`);
  console.log(`   - Krecher status: ${derivedFacts.krecher_status}${derivedFacts.krecher_end_year ? ` (ended ${derivedFacts.krecher_end_year})` : ''}\n`);

  // Walk src/ and check files
  const files = walkDir(SRC_DIR, ['.astro', '.md']);
  let totalErrors = 0;

  for (const file of files) {
    const errors = checkFile(file, derivedFacts);
    if (errors.length > 0) {
      const relativePath = file.replace(REPO_ROOT + '\\', '').replace(/\\/g, '/');
      console.log(`❌ ${relativePath}`);
      errors.forEach(err => {
        console.log(`   Line ${err.line}: "${err.claim}" — expected one of: ${JSON.stringify(err.expected)}`);
        console.log(`   Found: ${err.text}`);
      });
      console.log('');
      totalErrors += errors.length;
    }
  }

  if (totalErrors === 0) {
    console.log('✅ All claims verified against content/facts.yml and cv/data/architect.yml.');
    process.exit(0);
  } else {
    console.log(`❌ ${totalErrors} claim(s) failed verification.`);
    console.log('   → Update copy to match facts, or update content/facts.yml if the fact changed.\n');
    process.exit(1);
  }
}

main();
