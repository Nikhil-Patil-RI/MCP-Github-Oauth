# Development

## Set up your environment
First, let’s install uv and set up our Python project and environment:

```bash
MacOS/Linux : curl -LsSf https://astral.sh/uv/install.sh | sh
Windows : powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Make sure to restart your terminal afterwards to ensure that the uv command gets picked up.

Now, let’s create and set up our project:
### Running to local claude desktop app

1. Make sure you need to update claude_desktop_config.json to register tool

## you can find claude_desktop_config.json :
```bash
For Windows : code $env:AppData\Claude\claude_desktop_config.json
For Mac/Linux :code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```
```bash
{
  "mcpServers": {
    "Github-Oauth": {
      "command": "C:\\Users\\Hp\\.local\\bin\\uv",
      "args": [
        "--directory",
        "C:\\Users\\Hp\\Github-Oauth\\src\\github_oauth",
        "run",
        "server.py"
      ]
    }
  }
}
```
## Debugging 

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory C:\Users\Hp\Github-Oauth run github-oauth
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
