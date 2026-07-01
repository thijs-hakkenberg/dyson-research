#!/usr/bin/env node

/**
 * Repeated Trials Experiment for Paper 03
 *
 * Runs 5 independent trials of the deliberation system on 4 stratified questions.
 * Each trial starts fresh (no prior discussion state) and saves results to a
 * separate directory for analysis.
 *
 * Selected questions (stratified by convergence speed):
 *   - rq-0-14 (propellant-production-phase-0-scope) - 1 round (fastest)
 *   - rq-1-24 (swarm-coordination-architecture-scale) - 2 rounds (typical, technical)
 *   - rq-1-40 (slot-reallocation-governance) - 2 rounds (typical, governance)
 *   - rq-0-28 (isru-cost-methodology-validation) - 3 rounds (slowest)
 *
 * Usage:
 *   export $(cat .env | xargs)
 *   node publications/scripts/run_repeated_trials.js
 *   node publications/scripts/run_repeated_trials.js --question=propellant-production-phase-0-scope
 *   node publications/scripts/run_repeated_trials.js --trial=3
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { execFile } from 'child_process';
import { promisify } from 'util';

const execFileAsync = promisify(execFile);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');

// Configuration
const NUM_TRIALS = 5;
const QUESTIONS = [
	{
		slug: 'propellant-production-phase-0-scope',
		questionId: 'rq-0-14',
		phase: 'phase-0',
		dirName: 'rq-0-14-propellant-production-phase-0-scope',
		originalRounds: 1,
		category: 'technical-systems',
		stratification: 'fast'
	},
	{
		slug: 'swarm-coordination-architecture-scale',
		questionId: 'rq-1-24',
		phase: 'phase-1',
		dirName: 'rq-1-24-swarm-coordination-architecture-scale',
		originalRounds: 2,
		category: 'technical-systems',
		stratification: 'typical'
	},
	{
		slug: 'slot-reallocation-governance',
		questionId: 'rq-1-40',
		phase: 'phase-1',
		dirName: 'rq-1-40-slot-reallocation-governance',
		originalRounds: 2,
		category: 'governance',
		stratification: 'typical'
	},
	{
		slug: 'isru-cost-methodology-validation',
		questionId: 'rq-0-28',
		phase: 'phase-0',
		dirName: 'rq-0-28-isru-cost-methodology-validation',
		originalRounds: 3,
		category: 'economic',
		stratification: 'slow'
	}
];

const OUTPUT_BASE = path.join(PROJECT_ROOT, 'publications', 'data', 'repeated-trials');
const RQ_BASE = path.join(PROJECT_ROOT, 'src', 'content', 'research-questions');

/**
 * Copy directory recursively
 */
async function copyDir(src, dest) {
	await fs.mkdir(dest, { recursive: true });
	const entries = await fs.readdir(src, { withFileTypes: true });
	for (const entry of entries) {
		const srcPath = path.join(src, entry.name);
		const destPath = path.join(dest, entry.name);
		if (entry.isDirectory()) {
			await copyDir(srcPath, destPath);
		} else {
			await fs.copyFile(srcPath, destPath);
		}
	}
}

/**
 * Remove directory recursively
 */
async function removeDir(dirPath) {
	try {
		await fs.rm(dirPath, { recursive: true, force: true });
	} catch (e) {
		// Ignore if doesn't exist
	}
}

/**
 * Check if directory exists
 */
async function dirExists(dirPath) {
	try {
		const stat = await fs.stat(dirPath);
		return stat.isDirectory();
	} catch {
		return false;
	}
}

/**
 * Run a single trial for a question
 */
async function runTrial(question, trialNumber) {
	const discussionDir = path.join(RQ_BASE, question.phase, question.dirName);
	const backupDir = path.join(OUTPUT_BASE, '_backups', question.slug);
	const trialOutputDir = path.join(OUTPUT_BASE, question.slug, `trial-${trialNumber}`);

	console.log(`\n${'='.repeat(70)}`);
	console.log(`  Question: ${question.slug} (${question.stratification})`);
	console.log(`  Trial: ${trialNumber}/${NUM_TRIALS}`);
	console.log(`${'='.repeat(70)}`);

	// Step 1: Back up existing discussion data (only on first trial)
	if (trialNumber === 1 && await dirExists(discussionDir)) {
		console.log(`  Backing up existing discussion data...`);
		await removeDir(backupDir);
		await copyDir(discussionDir, backupDir);
	}

	// Step 2: Remove existing discussion.yaml, conclusion.md, and round dirs
	// (but keep the directory itself as it may contain the question .md)
	if (await dirExists(discussionDir)) {
		const entries = await fs.readdir(discussionDir);
		for (const entry of entries) {
			const entryPath = path.join(discussionDir, entry);
			if (entry === 'discussion.yaml' || entry === 'conclusion.md') {
				await fs.unlink(entryPath);
			} else if (entry.startsWith('round-')) {
				await removeDir(entryPath);
			}
		}
		console.log(`  Cleared previous discussion state.`);
	}

	// Step 3: Run the discussion
	console.log(`  Running discussion...`);
	const startTime = Date.now();

	try {
		const { stdout, stderr } = await execFileAsync(
			'node',
			[
				path.join(PROJECT_ROOT, 'scripts', 'run-discussion.js'),
				`--question=${question.slug}`,
				'--auto'
			],
			{
				cwd: PROJECT_ROOT,
				env: { ...process.env },
				timeout: 600000, // 10 minutes per trial
				maxBuffer: 10 * 1024 * 1024
			}
		);

		const duration = ((Date.now() - startTime) / 1000).toFixed(1);
		console.log(`  Completed in ${duration}s`);

		// Print key lines from stdout
		const lines = stdout.split('\n');
		for (const line of lines) {
			if (line.includes('Winner:') || line.includes('Termination') ||
				line.includes('Status:') || line.includes('Rounds completed') ||
				line.includes('Approval rate') || line.includes('terminating')) {
				console.log(`    ${line.trim()}`);
			}
		}

		if (stderr) {
			const errLines = stderr.split('\n').filter(l => l.trim());
			if (errLines.length > 0) {
				console.log(`  Stderr (${errLines.length} lines):`);
				for (const line of errLines.slice(0, 5)) {
					console.log(`    ${line}`);
				}
			}
		}

	} catch (error) {
		const duration = ((Date.now() - startTime) / 1000).toFixed(1);
		console.error(`  ERROR after ${duration}s: ${error.message}`);
		if (error.stdout) {
			const lastLines = error.stdout.split('\n').slice(-10);
			console.error('  Last stdout lines:');
			for (const line of lastLines) {
				console.error(`    ${line}`);
			}
		}
		// Don't throw - continue with other trials
		// Save whatever partial data exists
	}

	// Step 4: Copy results to trial output directory
	await fs.mkdir(trialOutputDir, { recursive: true });

	if (await dirExists(discussionDir)) {
		const entries = await fs.readdir(discussionDir);
		for (const entry of entries) {
			const srcPath = path.join(discussionDir, entry);
			const destPath = path.join(trialOutputDir, entry);

			if (entry === 'discussion.yaml' || entry === 'conclusion.md') {
				await fs.copyFile(srcPath, destPath);
			} else if (entry.startsWith('round-')) {
				await copyDir(srcPath, destPath);
			}
		}
		console.log(`  Saved trial results to: ${trialOutputDir}`);
	} else {
		console.log(`  WARNING: No discussion directory found after trial.`);
	}

	// Add trial metadata
	const metadata = {
		questionSlug: question.slug,
		questionId: question.questionId,
		trialNumber,
		timestamp: new Date().toISOString(),
		stratification: question.stratification,
		originalRounds: question.originalRounds,
		category: question.category
	};
	await fs.writeFile(
		path.join(trialOutputDir, 'trial-metadata.json'),
		JSON.stringify(metadata, null, 2),
		'utf-8'
	);

	return trialOutputDir;
}

/**
 * Restore original discussion data after all trials
 */
async function restoreOriginal(question) {
	const discussionDir = path.join(RQ_BASE, question.phase, question.dirName);
	const backupDir = path.join(OUTPUT_BASE, '_backups', question.slug);

	if (await dirExists(backupDir)) {
		console.log(`\n  Restoring original discussion data for ${question.slug}...`);

		// Clear current state
		if (await dirExists(discussionDir)) {
			const entries = await fs.readdir(discussionDir);
			for (const entry of entries) {
				const entryPath = path.join(discussionDir, entry);
				if (entry === 'discussion.yaml' || entry === 'conclusion.md') {
					await fs.unlink(entryPath);
				} else if (entry.startsWith('round-')) {
					await removeDir(entryPath);
				}
			}
		}

		// Copy backup back
		const entries = await fs.readdir(backupDir);
		for (const entry of entries) {
			const srcPath = path.join(backupDir, entry);
			const destPath = path.join(discussionDir, entry);
			const stat = await fs.stat(srcPath);
			if (stat.isDirectory()) {
				await copyDir(srcPath, destPath);
			} else {
				await fs.copyFile(srcPath, destPath);
			}
		}

		console.log(`  Restored.`);
	}
}

/**
 * Main execution
 */
async function main() {
	const args = process.argv.slice(2);
	const questionFilter = args.find(a => a.startsWith('--question='))?.split('=')[1];
	const trialFilter = args.find(a => a.startsWith('--trial='))?.split('=')[1];

	if (!process.env.DATABRICKS_TOKEN) {
		console.error('Error: DATABRICKS_TOKEN environment variable is required');
		console.error('Run: export $(cat .env | xargs)');
		process.exit(1);
	}

	console.log('='.repeat(70));
	console.log('  REPEATED TRIALS EXPERIMENT');
	console.log('  Paper 03: Multi-Model AI Consensus');
	console.log('='.repeat(70));
	console.log(`  Questions: ${QUESTIONS.length}`);
	console.log(`  Trials per question: ${NUM_TRIALS}`);
	console.log(`  Total runs: ${QUESTIONS.length * NUM_TRIALS}`);
	console.log(`  Output: ${OUTPUT_BASE}`);
	console.log();

	const questionsToRun = questionFilter
		? QUESTIONS.filter(q => q.slug === questionFilter || q.slug.includes(questionFilter))
		: QUESTIONS;

	if (questionsToRun.length === 0) {
		console.error(`No questions match filter: ${questionFilter}`);
		console.error('Available:', QUESTIONS.map(q => q.slug).join(', '));
		process.exit(1);
	}

	const startTrialNum = trialFilter ? parseInt(trialFilter) : 1;
	const startTime = Date.now();
	let completedTrials = 0;
	let failedTrials = 0;

	for (const question of questionsToRun) {
		console.log(`\n${'#'.repeat(70)}`);
		console.log(`# Question: ${question.slug}`);
		console.log(`# Stratification: ${question.stratification} (original: ${question.originalRounds} rounds)`);
		console.log(`${'#'.repeat(70)}`);

		for (let trial = startTrialNum; trial <= NUM_TRIALS; trial++) {
			try {
				await runTrial(question, trial);
				completedTrials++;
			} catch (error) {
				console.error(`  FATAL ERROR on trial ${trial}: ${error.message}`);
				failedTrials++;
			}

			// Brief pause between trials to avoid rate limiting
			if (trial < NUM_TRIALS) {
				console.log('  Waiting 5s before next trial...');
				await new Promise(r => setTimeout(r, 5000));
			}
		}

		// Restore original discussion data
		await restoreOriginal(question);
	}

	const totalDuration = ((Date.now() - startTime) / 1000 / 60).toFixed(1);

	console.log(`\n${'='.repeat(70)}`);
	console.log('  EXPERIMENT COMPLETE');
	console.log(`${'='.repeat(70)}`);
	console.log(`  Completed: ${completedTrials} trials`);
	console.log(`  Failed: ${failedTrials} trials`);
	console.log(`  Total duration: ${totalDuration} minutes`);
	console.log(`  Results saved to: ${OUTPUT_BASE}`);
	console.log();
}

main().catch(error => {
	console.error('Fatal error:', error);
	process.exit(1);
});
