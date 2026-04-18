# DeVILSona Documentation

This repository contains the comprehensive, MkDocs-generated knowledge base for **DeVILSona** — an immersive Virtual Reality simulation designed to transform how undergraduate engineering students engage with design thinking at Arizona State University.

Instead of reading static paper personas, students put on a Meta Quest headset and hold real-time, unscripted voice conversations with AI-driven characters to learn directly from the people their designs are meant to serve.

You can view the live documentation site here: **[DeVILSona Documentation](https://fse100capstone.github.io/DeVILSona-docs/)**

## 📚 Organization

The documentation is built with [MkDocs](https://www.mkdocs.org/) and the [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It is structured into distinct guides tailored to different audiences:

- **Educator Guide:** For instructors and project sponsors who run DeVILSona sessions in the classroom.
- **Admin Guide:** For IT staff and technical administrators managing deployment and infrastructure.
- **Developer Guide:** For incoming capstone development teams taking over the codebase.
- **Legacy:** Fine-grained technical documents covering specific subsystems and tooling in depth.

## 🛠️ Local Development

To run the documentation site locally and preview changes as you edit the Markdown files:

1. **Install Python** (3.8 or higher is recommended).
2. **Install the dependencies:**
   ```bash
   pip install mkdocs-material mkdocs-panzoom-plugin
   ```
3. **Start the development server:**
   ```bash
   mkdocs serve
   ```
4. **View the site:** Open your browser to `http://127.0.0.1:8000/DeVILSona-docs/` (or the address provided in your terminal).

The server will automatically reload whenever you save a Markdown (`.md`) file or update the `mkdocs.yml` configuration.

## 🚀 Deployment

This documentation is automatically deployed to GitHub Pages via GitHub Actions!

Whenever you merge or push changes to the `main` branch, the `.github/workflows/ci.yml` pipeline will trigger. It builds the site and pushes the static HTML to the `gh-pages` branch, which updates the live website within a minute or two.

## 📦 Related Repositories

- [**DeVILSona**](https://github.com/FSE100Capstone/DeVILSona): The primary VR simulation application (Unreal Engine 5).
- [**DeVILSona-infra**](https://github.com/FSE100Capstone/DeVILSona-infra): The cloud backend for session persistence (Terraform & AWS).
- [**DeVILStarter**](https://github.com/FSE100Capstone/DeVILStarter): The desktop launcher for infrastructure provisioning (Wails).
