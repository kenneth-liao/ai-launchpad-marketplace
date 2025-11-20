# Setting Up the AI Launchpad Marketplace Repository

## Push to GitHub

1. Create a new repository on GitHub named `ai-launchpad-marketplace`

2. Add the remote and push:
```bash
git remote add origin https://github.com/kenneth-liao/ai-launchpad-marketplace.git
git branch -M main
git push -u origin main
```

## For Users: Installing Plugins

### Option 1: Clone the Marketplace (Recommended)

Clone this repository to a location on your machine:

```bash
cd ~/projects  # or wherever you keep your repos
git clone https://github.com/kenneth-liao/ai-launchpad-marketplace.git
```

Then reference plugins in your Claude Code configuration by pointing to the cloned directory.

### Option 2: Direct GitHub Reference

Some Claude Code configurations may support direct GitHub references (check Claude Code documentation for current support).

## Adding New Plugins

When you create new plugins, add them to this repository following the same structure:

```bash
cd ai-launchpad-marketplace
mkdir your-plugin-name
# Add your plugin files
git add your-plugin-name/
git commit -m "Add your-plugin-name plugin"
git push
```

Don't forget to update the `.claude-plugin/marketplace.json` file to include your new plugin!
