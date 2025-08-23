# 🏥 Patients Management System API

A modern, robust REST API built with **FastAPI** for managing patient records with advanced features like BMI calculation, health verdicts, and comprehensive data validation.

## ✨ Features

- **🔄 Full CRUD Operations**: Create, Read, Update patient records
- **🧮 Smart Computations**: Automatic BMI calculation and health verdicts
- **✅ Data Validation**: Comprehensive input validation using Pydantic
- **📊 Sorting & Filtering**: Sort patients by height, weight, or BMI
- **🛡️ Error Handling**: Proper HTTP status codes and detailed error messages
- **💾 JSON Storage**: Simple file-based data persistence
- **📚 Auto-Generated Docs**: Interactive API documentation with Swagger UI

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and settings management
- **Python 3.8+** - Core programming language
- **Uvicorn** - Lightning-fast ASGI server
- **JSON** - Data storage format

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/patients-management-api.git
cd patients-management-api
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv

# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
uvicorn main:app --reload
```

### 5. Access Your API
- 🌐 **API Base URL**: `http://localhost:8000`
- 📖 **Interactive Docs**: `http://localhost:8000/docs`
- 📚 **Alternative Docs**: `http://localhost:8000/redoc`

## 📚 API Endpoints

### 🔍 **Read Operations**

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | Welcome message | None |
| `GET` | `/about` | API description | None |
| `GET` | `/view` | View all patients | None |
| `GET` | `/patient/{id}` | View specific patient | `id`: Patient ID |
| `GET` | `/sort` | Sort patients | `sort_by`, `order` |

### ✨ **Create Operations**

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/create` | Create new patient | `Patient` object |

### 🔄 **Update Operations**

| Method | Endpoint | Description | Parameters | Request Body |
|--------|----------|-------------|------------|--------------|
| `PUT` | `/edit/{patient_id}` | Update patient | `patient_id` | `PatientUpdate` object |

## 📊 Data Models

### Patient Model
```python
{
  "id": "P001",
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "gender": "Male",
  "height": 175.5,
  "weight": 70.5,
  "bmi": 22.9,        # Computed automatically
  "verdict": "Normal weight"  # Computed automatically
}
```

### Patient Update Model
```python
{
  "name": "John Smith",      # Optional
  "city": "Los Angeles",     # Optional
  "age": 31,                 # Optional
  "gender": "Male",          # Optional
  "height": 176.0,           # Optional
  "weight": 71.0             # Optional
}
```

## 🧮 Computed Fields

The API automatically calculates:

- **BMI (Body Mass Index)**: `weight / (height/100)²`
- **Health Verdict**:
  - Underweight: BMI < 18.5
  - Normal weight: 18.5 ≤ BMI < 24.9
  - Overweight: 25 ≤ BMI < 29.9
  - Obesity: BMI ≥ 30

## 📖 Usage Examples

### Create a New Patient
```bash
curl -X POST "http://localhost:8000/create" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "P001",
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "Male",
    "height": 175.5,
    "weight": 70.5
  }'
```

### View All Patients
```bash
curl http://localhost:8000/view
```

### View Specific Patient
```bash
curl http://localhost:8000/patient/P001
```

### Update Patient
```bash
curl -X PUT "http://localhost:8000/edit/P001" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 31,
    "weight": 72.0
  }'
```

### Sort Patients by BMI (Descending)
```bash
curl "http://localhost:8000/sort?sort_by=bmi&order=desc"
```

## 🔧 Configuration

### Data Storage
The application uses `patients.json` for data persistence. Create this file with sample data:

```json
{
  "P001": {
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "gender": "Male",
    "height": 175.5,
    "weight": 70.5
  }
}
```

### Environment Variables
No environment variables required - the app runs with default settings.

## 🧪 Testing

### Manual Testing
- Use the interactive Swagger UI at `/docs`
- Test with cURL commands
- Use Postman or similar API testing tools

### Automated Testing
```bash
# Install test dependencies
pip install pytest httpx

# Run tests (when you add them)
pytest
```

## 📁 Project Structure

```
patients-management-api/
├── main.py              # Main FastAPI application
├── patients.json        # Patient data storage
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore file
├── LICENSE             # MIT License
├── README.md           # Project documentation
└── venv/               # Virtual environment (not in git)
```

## 🚨 Error Handling

The API provides comprehensive error handling:

- **400 Bad Request**: Invalid input data or duplicate patient ID
- **404 Not Found**: Patient ID doesn't exist
- **422 Unprocessable Entity**: Validation errors
- **500 Internal Server Error**: Server-side issues

## 🔒 Data Validation

- **Age**: Must be between 1-119 years
- **Height**: Must be positive (in cm)
- **Weight**: Must be positive (in kg)
- **Gender**: Must be 'Male', 'Female', or 'Others'
- **ID**: Must be unique string

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@meet4041](https://github.com/meet4041)

## 🙏 Acknowledgments

- FastAPI community for the excellent framework
- Pydantic team for robust data validation
- Python community for the amazing ecosystem

## 📞 Support & Issues

- 🐛 **Bug Reports**: [Create an issue](https://github.com/meet4041/patients-management-api/issues)
- 💡 **Feature Requests**: [Create an issue](https://github.com/meet4041/patients-management-api/issues)
- 📚 **Documentation**: Check the [FastAPI docs](https://fastapi.tiangolo.com/)

## 🚀 Future Enhancements

- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Authentication & Authorization
- [ ] Patient search functionality
- [ ] Medical history tracking
- [ ] Appointment scheduling
- [ ] Report generation
- [ ] Docker containerization

---

⭐ **Star this repository if you find it helpful!**

🔗 **Connect with us**: [GitHub](https://github.com/meet4041) | [LinkedIn](https://www.linkedin.com/in/meetgandhi4041/)
