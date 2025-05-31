# METI Café - Anonymous Message Board

A simple Flask-based anonymous messaging application with admin moderation features.

## Features

- 🗨️ Anonymous messaging with real-time updates
- 🕒 Timestamp display on hover
- 🔒 Password-protected admin panel for message deletion
- 📱 Responsive design
- 🔗 Automatic URL detection and linking
- 🔔 Sound notifications for new messages
- 🍽️ Restaurant menus on demand – type /menus in the chat to view a list of nearby restaurants and their menus

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd meti-cafe
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your actual values:
   ```bash
   # Generate a secure secret key
   FLASK_SECRET_KEY=your-super-secret-random-key-here-change-this
   
   # Set your admin password
   ADMIN_PASSWORD=your-chosen-admin-password
   ```

### 4. Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## 5. Testing 
| Description | Test Input | Expected output |
|---|---|---|
| Send no message | press submit with empty text field | pop message saying please fill the text field |
| Send one word/sentence | Hello | Hello |
| Send multiline input | Hello \n Hi | Hello \n Hi |
| Send a link |https://drive.google.com/drive/folders/1c4B-X1Ejsvajc2TGT1eG4K-o9t3gfunq|https://drive.google.com/drive/folders/1c4B-X1Ejsvajc2TGT1eG4K-o9t3gfunq| 
| Sound | Send any message | Hear the sound |
| Responsivness | Send any message | the message appears immediatly to other users without refreshing |
| Hossam's Special Test | Send the triger | it must be sent correctly |
|The /menus feature| send /menus (can be lowercase or uppercase)| A window with a list of menus will appear |

## Admin Access

- Visit `/amin-delete` to access the admin panel
- Enter the password you set in your `.env` file
- Delete unwanted messages using the 🗑️ button

## File Structure

```
meti-cafe/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Main chat interface
│   └── admin_login.html  # Admin login page
├── static/               # Static files (CSS, JS, images)
├── .env                  # Environment variables (not tracked)
├── .env.example         # Example environment file
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Security Notes

- Never commit your `.env` file to version control
- Use a strong, randomly generated secret key
- Change the default admin password
- Consider using HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
