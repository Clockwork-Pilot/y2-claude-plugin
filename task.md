# Task: task_1

## Project

# Project Description
Claude Code Plugin - A Python-based plugin system that extends Claude Code with advanced document management and task lifecycle tracking capabilities.

Key Components:
1. Knowledge Base Tool: API-first knowledge base system using JSON Patch operations (RFC 6902) with automatic markdown rendering. Features atomic file writes, file protection with read-only attributes, and pluggable RenderableModel classes for document rendering.

2. Task Lifecycle Tool: Iteration-based task management system for tracking task execution through numbered iterations with automatic metrics collection. Collects code metrics from git diff (files changed, lines added/removed) and test metrics from pytest (pass rate, coverage). Tasks progress through iterations until metrics stabilize.

3. Hook System: Implements comprehensive hook handlers for Claude Code lifecycle events, logging all invocations for debugging and monitoring.

Project Structure:
- knowledge_tool (Git submodule): Core knowledge base system
- pycov (Git submodule): Python coverage utilities
- lifecycle_tool: Task lifecycle management with knowledge models
- Configurable hook handlers for extensibility

Features:
- Atomic JSON Patch operations with automatic validation
- Automatic markdown document generation
- Read-only file protection to prevent accidental modifications
- Iteration-based metrics collection and analysis
- Plugin-friendly architecture with modular handlers

**Created At:** 2026-03-02T11:57:57.644681

**Updated At:** 2026-03-05T00:00:00.000000

## Overview
Claude Code Plugin is a Python-based plugin system that extends Claude Code with enterprise-grade capabilities for knowledge base management and task lifecycle tracking.

## Key Components
### Knowledge Base Tool
API-first knowledge base system using JSON Patch operations (RFC 6902) with automatic markdown rendering. Features atomic file writes, file protection, and pluggable RenderableModel classes.

#### Knowledge Tool Configuration
Configuration guide for the Knowledge Base Tool pluggable model system.

**Configuration File:** knowledge_config.yaml

**Location:** Same directory as apply_json_patch.py script

##### Overview
This file configures pluggable model directories for the knowledge tool. Place this file in the same directory as apply_json_patch.py script, or set KNOWLEDGE_TOOL_CONFIG_ROOT environment variable to override the config location.

The knowledge tool always loads built-in models. External models from pluggable_models_dirs are merged with built-in models.

##### Pluggable Models Directories
List of directories containing custom/pluggable knowledge models. Paths are relative to this config file location.

**Format:** List of directory paths

**Examples:**
  - ./models
  - ./custom_models
  - /absolute/path/to/models

##### Built-in Models
The knowledge tool always loads the following built-in models: Doc (default document model), Task (task with plan and iterations), Iteration (task iteration with metrics).

##### Model Merging
External models from pluggable_models_dirs are merged with built-in models. If a custom model has the same name as a built-in model, the custom model takes precedence.

##### Environment Variable Override
Set KNOWLEDGE_TOOL_CONFIG_ROOT environment variable to specify a custom config file location. This overrides the default location (same directory as apply_json_patch.py).

**Variable Name:** KNOWLEDGE_TOOL_CONFIG_ROOT

**Usage:** export KNOWLEDGE_TOOL_CONFIG_ROOT=/path/to/config

### Task Lifecycle Tool
Iteration-based task management system with automatic metrics collection from git and pytest. Tasks progress through iterations until metrics stabilize, then archive to history.

### Hook System
Comprehensive hook handlers for Claude Code lifecycle events with modular handler structure and event logging for debugging and monitoring.

## Architecture
Multi-component architecture with Git submodules (knowledge_tool, pycov) and local modules (lifecycle_tool, hooks). Pluggable models with RenderableModel base class for custom document rendering.

## Key Features
Atomic JSON Patch operations with automatic validation, automatic markdown document generation from JSON source, read-only file protection, iteration-based metrics collection and analysis, plugin-friendly modular architecture, filtering of temporary files from knowledge registry, task-based knowledge document management.

## Technology Stack
Python 3.11+, Pydantic for data validation, RFC 6902 JSON Patch for document operations, Markdown auto-generation from JSON, Integration with Git, pytest, and fastmcp.


## Plan

# Task Plan
Updated task plan with project description

**Created At:** 2026-03-02T11:57:57.644681

**Updated At:** 2026-03-02T11:57:57.644681

**Test:** 1