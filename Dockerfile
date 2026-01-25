{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "test_db",
      "type": "python",
      "request": "launch",

      "module": "scripts.test_db",

      "cwd": "${workspaceFolder}/dev",

      "env": {
        "PYTHONPATH": "${workspaceFolder}/dev"
      },

      "console": "integratedTerminal"
    }
  ]
}