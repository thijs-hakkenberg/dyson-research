#!/usr/bin/env node
/**
 * Recount trade-offs and divergent topics from saved aggregation baseline results.
 *
 * Uses improved heuristics that handle:
 * - Aggregation syntheses: "## 3. Trade-offs and Competing Positions" with sub-headings or bullet items
 * - Deliberation conclusions: "## Unresolved Questions" with numbered items, plus inline trade-offs in Key Points
 */

const fs = require('fs');
const path = require('path');

const RESULTS_PATH = path.join(__dirname, '..', 'drafts', '03-multi-model-ai-consensus', 'aggregation-baseline-results.json');
const BASE_DIR = path.join(__dirname, '..', '..', 'src', 'content', 'research-questions');

function stripFrontmatter(content) {
  const match = content.match(/^---\n[\s\S]*?\n---\n/);
  return match ? content.slice(match[0].length).trim() : content.trim();
}

/**
 * Count trade-offs in an aggregation synthesis.
 *
 * The synthesis format has "## 3. Trade-offs and Competing Positions"
 * with either:
 * - ### sub-headings (each = one trade-off)
 * - Numbered items (1., 2., etc.)
 * - Bold bullet items (- **item**)
 */
function countTradeoffsInSynthesis(text) {
  const lines = text.split('\n');
  let inTradeoffSection = false;
  let subheadingCount = 0;
  let numberedCount = 0;
  let boldParaCount = 0;

  for (const line of lines) {
    const trimmed = line.trim();

    // Detect trade-off section header (various formats)
    if (/^##\s+(\d+\.\s*)?trade[- ]?off/i.test(trimmed) ||
        /^##\s+(\d+\.\s*)?competing\s+positions/i.test(trimmed) ||
        /^##\s+(\d+\.\s*)?.*trade[- ]?off.*competing/i.test(trimmed)) {
      inTradeoffSection = true;
      continue;
    }

    // Detect end of section (next ## heading that's not a trade-off heading)
    if (inTradeoffSection && /^##\s+/.test(trimmed) && !/^###/.test(trimmed) &&
        !/trade[- ]?off/i.test(trimmed)) {
      inTradeoffSection = false;
      continue;
    }

    if (inTradeoffSection) {
      // Sub-headings (###) each represent a distinct trade-off topic
      if (/^###\s+/.test(trimmed)) {
        subheadingCount++;
      }
      // Top-level numbered items (not within a sub-heading context)
      else if (/^\d+[\.\)]\s+\*\*/.test(trimmed)) {
        numberedCount++;
      }
      // Bold paragraphs starting a new trade-off topic (when no ### used)
      // These look like: **Topic Name:** or **Topic Name.**
      else if (/^\*\*[^*]+\*\*/.test(trimmed) && trimmed.length > 20 &&
               !/^[-*]\s+\*\*Position/i.test(trimmed)) {
        // Only count if it's a topic header, not a position statement
        // Position statements start with "- **Position A" or similar
        boldParaCount++;
      }
    }
  }

  // Prefer sub-headings if present; otherwise fall back to numbered/bold items
  if (subheadingCount > 0) return subheadingCount;
  if (numberedCount > 0) return numberedCount;
  if (boldParaCount > 0) return boldParaCount;

  // Fallback: count paragraphs with competing position language
  let inSection = false;
  let paraCount = 0;
  let blankLast = true;

  for (const line of lines) {
    const trimmed = line.trim();
    if (/^##\s+.*trade[- ]?off/i.test(trimmed)) {
      inSection = true;
      continue;
    }
    if (inSection && /^##\s+/.test(trimmed) && !/^###/.test(trimmed) &&
        !/trade[- ]?off/i.test(trimmed)) {
      inSection = false;
      continue;
    }
    if (inSection) {
      if (trimmed === '') {
        blankLast = true;
      } else if (blankLast && trimmed.length > 30) {
        if (/\b(versus|vs\.|while|whereas|alternatively|competing|disagree|diverge|contrast)\b/i.test(trimmed)) {
          paraCount++;
        }
        blankLast = false;
      } else {
        blankLast = false;
      }
    }
  }
  return paraCount;
}

/**
 * Count distinct trade-offs in a deliberation conclusion.
 *
 * The conclusion format has "## Key Points" with bullet items. Trade-offs are
 * identified by language indicating competing positions within key points,
 * and also in the body text discussing areas of disagreement.
 */
function countTradeoffsInConclusion(text) {
  const lines = text.split('\n');
  let tradeoffCount = 0;

  // Count bullet items in Key Points that describe trade-offs
  let inKeyPoints = false;
  for (const line of lines) {
    const trimmed = line.trim();

    if (/^##\s+Key\s+Points/i.test(trimmed)) {
      inKeyPoints = true;
      continue;
    }
    if (inKeyPoints && /^##\s+/.test(trimmed)) {
      inKeyPoints = false;
      continue;
    }

    if (inKeyPoints && /^[-*]\s+\*\*/.test(trimmed)) {
      // Check if this key point describes competing approaches
      const fullLine = trimmed.toLowerCase();
      if (/\b(versus|vs\.|trade[- ]?off|rather than|instead of|while|whereas|competing|tension|balance|between .* and)\b/.test(fullLine)) {
        tradeoffCount++;
      }
    }
  }

  // Also count explicit trade-off mentions in the Summary section
  let inSummary = false;
  const summaryTradeoffs = new Set();
  for (const line of lines) {
    const trimmed = line.trim();
    if (/^##\s+Summary/i.test(trimmed)) {
      inSummary = true;
      continue;
    }
    if (inSummary && /^##\s+/.test(trimmed)) {
      inSummary = false;
      continue;
    }
    if (inSummary) {
      // Count sentences with explicit trade-off language
      const matches = trimmed.match(/\btrade[- ]?off\b/gi) || [];
      if (matches.length > 0) {
        summaryTradeoffs.add(line.substring(0, 50)); // dedup by first 50 chars
      }
    }
  }

  return tradeoffCount + summaryTradeoffs.size;
}

/**
 * Count unresolved/divergent topics.
 * Deliberation conclusions use: "## Unresolved Questions" with numbered items (1. **Bold**)
 * Aggregation syntheses use: "## 4. Unresolved Questions" with bold paragraphs (**What is...**)
 */
function countDivergentTopics(text) {
  const lines = text.split('\n');
  let inSection = false;
  let count = 0;

  for (let i = 0; i < lines.length; i++) {
    const trimmed = lines[i].trim();

    // Match various unresolved/open question section headers
    if (/^##\s+(\d+\.\s*)?unresolved/i.test(trimmed) ||
        /^##\s+(\d+\.\s*)?open\s+question/i.test(trimmed) ||
        /^##\s+(\d+\.\s*)?divergent/i.test(trimmed)) {
      inSection = true;
      continue;
    }

    // End of section: next ## heading (but not ###)
    if (inSection && /^##\s+/.test(trimmed) && !/^###/.test(trimmed) &&
        !/unresolved/i.test(trimmed) && !/open\s+question/i.test(trimmed)) {
      inSection = false;
      continue;
    }

    if (inSection) {
      // Numbered items: "1. **Bold title**"
      if (/^\d+[\.\)]\s+\*\*/.test(trimmed)) {
        count++;
      }
      // Regular numbered items without bold
      else if (/^\d+[\.\)]\s+[A-Z]/.test(trimmed) && trimmed.length > 20) {
        count++;
      }
      // Bullet items with bold
      else if (/^[-*]\s+\*\*/.test(trimmed) && trimmed.length > 20) {
        count++;
      }
      // Bold paragraph starters: "**What is the...?**" (used in aggregation syntheses)
      else if (/^\*\*[^*]+\*\*/.test(trimmed) && trimmed.length > 20) {
        count++;
      }
    }
  }

  return count;
}

// ── Main ───────────────────────────────────────────────────────────────────────
const data = JSON.parse(fs.readFileSync(RESULTS_PATH, 'utf-8'));

console.log('Recounting with improved heuristics...\n');

const QUESTIONS = data.results.map(r => r.question);
const synthMap = {};
data.syntheses.forEach(s => { synthMap[s.question] = s.synthesis; });

const updated = [];

for (const r of data.results) {
  if (r.error) {
    updated.push(r);
    continue;
  }

  const synthesis = synthMap[r.question];
  const conclusionPath = path.join(BASE_DIR, r.question, 'conclusion.md');
  const conclusion = stripFrontmatter(fs.readFileSync(conclusionPath, 'utf-8'));

  const aggTradeoffs = countTradeoffsInSynthesis(synthesis);
  const aggDivergent = countDivergentTopics(synthesis);
  const delibTradeoffs = countTradeoffsInConclusion(conclusion);
  const delibDivergent = countDivergentTopics(conclusion);

  const result = {
    question: r.question,
    name: r.name,
    aggregation: {
      tradeoffs: aggTradeoffs,
      divergentTopics: aggDivergent,
      synthesisLength: r.aggregation.synthesisLength,
    },
    deliberation: {
      tradeoffs: delibTradeoffs,
      divergentTopics: delibDivergent,
      conclusionLength: r.deliberation.conclusionLength,
    },
    delta: {
      tradeoffs: delibTradeoffs - aggTradeoffs,
      divergentTopics: delibDivergent - aggDivergent,
    },
  };

  updated.push(result);

  console.log(`${r.name.padEnd(48)} Agg(T=${aggTradeoffs}/D=${aggDivergent})  Delib(T=${delibTradeoffs}/D=${delibDivergent})  Delta(T=${result.delta.tradeoffs}/D=${result.delta.divergentTopics})`);
}

// Update the results file
data.results = updated;

// Recompute summary
const successful = updated.filter(r => !r.error);
const mean = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
const sum = arr => arr.reduce((a, b) => a + b, 0);

const aggT = successful.map(r => r.aggregation.tradeoffs);
const delT = successful.map(r => r.deliberation.tradeoffs);
const aggD = successful.map(r => r.aggregation.divergentTopics);
const delD = successful.map(r => r.deliberation.divergentTopics);

data.summary.aggregationMeans = { tradeoffs: mean(aggT).toFixed(2), divergentTopics: mean(aggD).toFixed(2) };
data.summary.deliberationMeans = { tradeoffs: mean(delT).toFixed(2), divergentTopics: mean(delD).toFixed(2) };
data.summary.aggregationTotals = { tradeoffs: sum(aggT), divergentTopics: sum(aggD) };
data.summary.deliberationTotals = { tradeoffs: sum(delT), divergentTopics: sum(delD) };
data.summary.deliberationBetter = {
  tradeoffs: successful.filter(r => r.delta.tradeoffs > 0).length,
  divergentTopics: successful.filter(r => r.delta.divergentTopics > 0).length,
};
data.summary.aggregationBetter = {
  tradeoffs: successful.filter(r => r.delta.tradeoffs < 0).length,
  divergentTopics: successful.filter(r => r.delta.divergentTopics < 0).length,
};
data.summary.tied = {
  tradeoffs: successful.filter(r => r.delta.tradeoffs === 0).length,
  divergentTopics: successful.filter(r => r.delta.divergentTopics === 0).length,
};

fs.writeFileSync(RESULTS_PATH, JSON.stringify(data, null, 2));

console.log('\n=== SUMMARY ===');
console.log(`Mean trade-offs:    Agg=${data.summary.aggregationMeans.tradeoffs}  Delib=${data.summary.deliberationMeans.tradeoffs}`);
console.log(`Mean divergent:     Agg=${data.summary.aggregationMeans.divergentTopics}  Delib=${data.summary.deliberationMeans.divergentTopics}`);
console.log(`Total trade-offs:   Agg=${data.summary.aggregationTotals.tradeoffs}  Delib=${data.summary.deliberationTotals.tradeoffs}`);
console.log(`Total divergent:    Agg=${data.summary.aggregationTotals.divergentTopics}  Delib=${data.summary.deliberationTotals.divergentTopics}`);
console.log(`Delib better (T):   ${data.summary.deliberationBetter.tradeoffs}/${successful.length}`);
console.log(`Agg better (T):     ${data.summary.aggregationBetter.tradeoffs}/${successful.length}`);
console.log(`Tied (T):           ${data.summary.tied.tradeoffs}/${successful.length}`);
console.log(`Delib better (D):   ${data.summary.deliberationBetter.divergentTopics}/${successful.length}`);
console.log(`Agg better (D):     ${data.summary.aggregationBetter.divergentTopics}/${successful.length}`);
console.log(`Tied (D):           ${data.summary.tied.divergentTopics}/${successful.length}`);

console.log('\nResults updated in:', RESULTS_PATH);
