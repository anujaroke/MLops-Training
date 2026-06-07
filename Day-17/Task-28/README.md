# AI LeetCode Mentor

## Overview

AI LeetCode Mentor is an automation workflow built using n8n, SERPER API, and OpenRouter.

The workflow accepts a LeetCode problem number, identifies the corresponding problem using SERPER, and generates detailed study notes using a Large Language Model.

## Features

* Search LeetCode problems using problem number
* Automatic problem discovery
* AI-generated explanations
* ELI10 summaries
* Brute Force and Optimal approaches
* Time and Space Complexity analysis
* Python solution generation
* Dry run examples

## Tech Stack

* n8n
* SERPER API
* OpenRouter
* DeepSeek V3

## Workflow

Problem Number → SERPER API → Problem Discovery → DeepSeek V3 → Structured Study Notes

## Example

Input:

300

### Output:

* Longest Increasing Subsequence
* ELI10 Explanation
* Optimal Approach
* Complexity Analysis
* Python Solution
* Dry Run Example

## Future Improvements

* Export notes to Google Docs
* Add support for LeetCode URLs as input
* Build a simple web interface