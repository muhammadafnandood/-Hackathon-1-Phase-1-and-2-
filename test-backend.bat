@echo off
echo Testing Backend Login API...
echo.

curl -X POST http://127.0.0.1:8000/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\":\"Test\",\"last_name\":\"User\",\"email\":\"test@example.com\",\"password\":\"test123\"}"

echo.
echo.
echo Login Test:
curl -X POST http://127.0.0.1:8000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\"}"

echo.
echo.
pause
