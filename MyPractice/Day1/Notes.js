// ### Ollama – Brief Overview
// Ollama is a tool that allows you to run AI language models locally on your computer without relying on paid cloud APIs.

// ### Key Points
// * Local AI: Run models directly on your laptop.
// * Free: No API charges for local usage.
// * Privacy: Your prompts and responses can stay on your computer.
// * Supports models: Qwen, Llama, Mistral, Gemma, etc.
// * Developer-friendly: Integrate AI into Node.js, Python, and other applications.

// ### Important Commands
// | Command               | Purpose                 |
// | --------------------- | ----------------------- |
// | `ollama list`         | Show installed models   |
// | `ollama run qwen3:4b` | Run AI model            |
// | `ollama pull model`   | Download model          |
// | `ollama rm model`     | Delete model            |
// | `ollama ps`           | Show running models     |
// | `ollama serve`        | Start API server        |
// | `ollama --help`       | Show available commands |

// ### Example for Your VerbaFlow Project
// Your Node.js Backend
//         ↓
// Ollama API
//         ↓
// Qwen3:4b Model
//         ↓
// AI Response
// Example: User speaks English → Backend sends text to Qwen3 → AI checks grammar → Frontend displays feedback.
// In simple terms: **Ollama is like a local AI engine that lets you run models such as Qwen3 on your own computer.

// Day1 Lecture(1) Notes:
// ollama --help 
// ollama run phi3 model
