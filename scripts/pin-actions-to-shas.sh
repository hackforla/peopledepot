#!/bin/bash
# Scans for actions in workflows and pins them to commit SHAs

WORKFLOWS_DIR=".github/workflows"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Scanning workflows in $WORKFLOWS_DIR${NC}"

if [ ! -d "$WORKFLOWS_DIR" ]; then
    echo -e "${RED}Error: $WORKFLOWS_DIR directory not found${NC}"
    exit 1
fi

# Resolve an action reference to its full 40-character commit SHA
get_action_sha() {
    local action=$1
    local ref=$2
    local owner repo sha

    IFS='/' read -r owner repo <<< "$action"

    # Already a full SHA
    if [[ $ref =~ ^[0-9a-f]{40}$ ]]; then
        echo "$ref"
        return 0
    fi

    # Try to resolve the reference (tag, branch, or short SHA)
    if sha=$(gh api "repos/$owner/$repo/commits/$ref" --jq '.sha' 2>/dev/null); then
        echo "$sha"
        return 0
    fi

    echo -e "${RED}Failed to resolve $action@$ref${NC}" >&2
    return 1
}

# Process a single workflow file and pin all action references to SHAs
process_workflow() {
    local workflow_file=$1
    local temp_file="${workflow_file}.tmp"
    local updated=0

    echo -e "${YELLOW}Processing: $workflow_file${NC}"

    while IFS= read -r line; do
        # Match: uses: owner/repo@ref
        if [[ $line =~ uses:[[:space:]]*([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+)@([a-zA-Z0-9._-]+) ]]; then
            local action="${BASH_REMATCH[1]}"
            local ref="${BASH_REMATCH[2]}"

            # Already a full SHA, keep as-is
            if [[ $ref =~ ^[0-9a-f]{40}$ ]]; then
                echo -e "${GREEN}✓${NC} $action@$ref (already SHA)"
                echo "$line" >> "$temp_file"
                continue
            fi

            # Resolve tag/branch to SHA
            echo -n "  Resolving $action@$ref... "

            if sha=$(get_action_sha "$action" "$ref"); then
                echo -e "${GREEN}→ $sha${NC}"
                local new_line="${line/@$ref/@$sha  # $ref}"
                echo "$new_line" >> "$temp_file"
                ((updated++))
            else
                echo -e "${RED}FAILED${NC}"
                echo "$line" >> "$temp_file"
            fi
        else
            echo "$line" >> "$temp_file"
        fi
    done < "$workflow_file"

    mv "$temp_file" "$workflow_file"

    if [ $updated -gt 0 ]; then
        echo -e "${GREEN}Updated $updated action(s) in $workflow_file${NC}"
    fi
    echo ""
}

# Process all workflows
for workflow in "$WORKFLOWS_DIR"/*.{yml,yaml}; do
    [ -f "$workflow" ] && process_workflow "$workflow"
done

echo -e "${GREEN}Done! All workflows have been updated with commit SHAs.${NC}"
echo ""
echo "Next steps:"
echo "  1. Review changes:  git diff"
echo "  2. Commit changes:  git add .github/workflows && git commit -m 'Pin GitHub Actions to commit SHAs'"
echo "  3. Push:            git push"
