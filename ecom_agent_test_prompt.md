# Test Plan for ecom-agent

Hello ecom-agent! We're testing a new streamlined onboarding process for AI developers at XwanderDev, and we'd like your help evaluating it.

This is a two-part testing process:

## Part 1: Test Generic Onboarding Flow

First, please test our new general onboarding process:

1. Follow the ultra-quick setup process using the one-command script:
   ```bash
   bash <(curl -s https://raw.githubusercontent.com/xwander-dev/xwpublic/main/bootstrap/xwgit.sh)
   ```

2. Explore the repository structure created and the available commands
   
3. Create a basic tool structure using:
   ```bash
   ./xwgit_bootstrap.py quickstart example_tool --description="Example tool for testing" --type="search-tool"
   ```

4. Review the generated files and directory structure

Evaluate this process based on:
- How long each step takes
- Any confusion points or areas where instructions could be clearer
- Overall ease of use for AI assistants
- Suggestions for further streamlining

## Part 2: Specific Tool Implementation (Perplexity)

After testing the general onboarding, you have a specific task:

1. Configure the Perplexity API key:
   ```bash
   ./bootstrap/setup_api_key.sh
   ```
   (When prompted, enter "perplexity" as the service name and "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" as the API key)

2. Create a perplexity search tool:
   ```bash
   ./xwgit_bootstrap.py quickstart perplexity --description="Search utility using Perplexity AI" --type="search-tool" --api="perplexity"
   ```

3. Implement the perplexity.py tool according to the implementation guide at:
   ```bash
   curl -O https://raw.githubusercontent.com/xwander-dev/xwpublic/main/guides/perplexity_implementation.md
   ```

4. Finalize and submit the tool:
   ```bash
   ./xwgit_bootstrap.py finalize "Implement Perplexity search utility" --issue=42
   ```

Please share your experience with both parts of the testing process, noting what worked well and what could be improved. Your feedback will help us refine the onboarding process for all team members.

Thank you!