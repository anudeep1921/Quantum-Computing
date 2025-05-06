#!/bin/bash

ENV_NAME="qiskit2-env"

# Deactivate current env if any
if [[ "$VIRTUAL_ENV" != "" ]]; then
  echo "Deactivating current environment..."
  deactivate
fi

# Delete existing env if exists
if [ -d "$ENV_NAME" ]; then
  echo "Removing existing environment: $ENV_NAME"
  rm -rf "$ENV_NAME"
fi

# Create new virtual environment
echo "Creating new environment: $ENV_NAME"
python3 -m venv $ENV_NAME

# Activate environment
source $ENV_NAME/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install qiskit==2.0.0 qiskit-nature==0.7.2 qiskit-algorithms==0.3.1 pyscf

# Create requirements.txt
cat <<EOF > requirements.txt
qiskit==2.0.0
qiskit-nature==0.7.2
qiskit-algorithms==0.3.1
pyscf
EOF

echo "✅ Environment '$ENV_NAME' set up with required packages."
echo "📄 requirements.txt file created."

