import 'package:flutter/material.dart';
import 'package:mainapp/Login/pass.dart';
import 'package:pinput/pinput.dart';

class VerifyOtpPage extends StatelessWidget {
  const VerifyOtpPage({super.key});

  @override
  Widget build(BuildContext context) {
    final defaultPinTheme = PinTheme(
      width: 50,
      height: 60,
      textStyle: const TextStyle(
        fontSize: 20,
        color: Colors.black,
      ),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
        borderRadius: BorderRadius.circular(8),
      ),
    );

    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                "NIA",
                style: TextStyle(
                  fontSize: 128,
                  color: Color(0xFF2C45D5),
                  fontWeight: FontWeight.w400,
                  fontFamily: "Julius",
                ),
              ),
              const SizedBox(height: 20),
              Image.asset('assets/logo.png',
                  width: 175, height: 175 // Replace with your image path
                  ),
              const SizedBox(height: 30),
              const Text(
                "Enter the OTP sent to your mobile",
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 20),

              // OTP Input Field (Pinput)
              Pinput(
                length: 6,
                defaultPinTheme: defaultPinTheme,
                onCompleted: (pin) {
                  print('OTP Entered: $pin');
                },
              ),

              const SizedBox(height: 30),

              ElevatedButton(
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => passWord()),
                  );
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF2C45D5),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  minimumSize: const Size(double.infinity, 48),
                ),
                child: const Text(
                  "Verify",
                  style: TextStyle(fontSize: 16, color: Colors.white),
                ),
              ),

              const SizedBox(height: 16),

              GestureDetector(
                onTap: () {
                  // Resend OTP logic
                },
                child: const Text(
                  "Resend OTP",
                  style: TextStyle(
                    color: Color(0xFF2C45D5),
                    decoration: TextDecoration.none,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
