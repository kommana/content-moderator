# Content Moderator

A powerful, user-friendly web application for real-time content moderation using advanced machine learning techniques. This tool helps identify and analyze potentially harmful content across multiple risk categories.

## 🎯 Purpose
Designed to help content managers, community moderators, and developers ensure safer online spaces by providing instant analysis of text content for various types of harmful content.

## ✨ Key Features
- **Real-time Analysis**: Instant content moderation with visual feedback
- **Multi-Category Detection**: Analyzes content across five key categories:
  - Harassment
  - Hate Speech
  - Self-harm
  - Sexual Content
  - Violence
- **Adjustable Safety Thresholds**: Customize moderation sensitivity based on your needs
- **Visual Risk Assessment**: Clear graphical representation of risk levels
- **Scientific Notation**: Precise risk measurements for accurate assessment
- **Modern UI/UX**: Clean, intuitive interface with responsive design
- **Detailed Reports**: Comprehensive analysis with percentage-based risk levels

## 🛠️ Technical Details
Built using:
- Flask for the backend server
- Hugging Face's Gradio client for ML model integration
- Matplotlib for data visualization
- Modern HTML/CSS for the frontend interface

## 🎓 Credits
This project utilizes the content moderation model created by [Duc Haba](https://huggingface.co/duchaba), hosted on Hugging Face Spaces.

## 📝 License
MIT License - Copyright (c) 2024 Raj Kommana

## 🎯 Use Cases
- Content Management Systems
- Social Media Platforms
- Educational Institutions
- Online Communities
- Customer Service Platforms
- Forum Moderation
- Comment Section Management

## 🔒 Privacy
All content analysis is performed in real-time without storing any user data.


## Features

- Real-time content moderation
- Visual representation of risk levels
- Adjustable safety threshold
- Clean and modern user interface
- Detailed analysis results

## Credits

This project uses the content moderation model created by [Duc Haba](https://huggingface.co/duchaba). The model is hosted on Hugging Face Spaces and is used through their API.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/content-moderator.git
cd content-moderator
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Usage

1. Open your web browser and navigate to `http://localhost:5000`
2. Enter the text you want to analyze
3. Adjust the safety threshold if needed
4. Click "Analyze Content" to see the results

## Requirements

See `requirements.txt` for a full list of dependencies.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Raj Kommana

## Acknowledgments

- [Duc Haba](https://huggingface.co/duchaba) for the content moderation model
- Hugging Face for hosting the model and providing the API 