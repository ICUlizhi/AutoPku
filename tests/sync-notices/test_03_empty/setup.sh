#!/bin/bash
set -e
mkdir -p test00/太极拳
mkdir -p fixtures
cat > fixtures/mock_assignments.txt << 'EOF'
太极拳
EOF
echo "setup complete"
