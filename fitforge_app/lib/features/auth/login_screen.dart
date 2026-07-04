import 'package:flutter/material.dart';
import '../../core/services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() =>
      _LoginScreenState();
}

class _LoginScreenState
    extends State<LoginScreen> {
  final TextEditingController emailController =
      TextEditingController();

  final TextEditingController passwordController =
      TextEditingController();

  final FocusNode emailFocus =
      FocusNode();

  final FocusNode passwordFocus =
      FocusNode();

  Future<void> login() async {
    final result =
        await AuthService.login(
      emailController.text.trim(),
      passwordController.text.trim(),
    );

    print(result);

    if (!mounted) return;

    if (result.containsKey('access')) {
      print("LOGIN SUCCESS");

      Navigator.pushReplacementNamed(
        context,
        '/dashboard',
      );
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(
        const SnackBar(
          content: Text(
            'Invalid Email or Password',
          ),
        ),
      );
    }
  }

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    emailFocus.dispose();
    passwordFocus.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SizedBox(
          width: 450,
          child: Card(
            child: Padding(
              padding:
                  const EdgeInsets.all(30),
              child: Column(
                mainAxisSize:
                    MainAxisSize.min,
                children: [
                  const Text(
                    "FITFORGE",
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight:
                          FontWeight.bold,
                    ),
                  ),

                  const SizedBox(
                      height: 30),

                  TextField(
                    controller:
                        emailController,
                    focusNode: emailFocus,
                    textInputAction:
                        TextInputAction.next,
                    onSubmitted: (_) {
                      FocusScope.of(
                        context,
                      ).requestFocus(
                        passwordFocus,
                      );
                    },
                    decoration:
                        const InputDecoration(
                      hintText: "Email",
                    ),
                  ),

                  const SizedBox(
                      height: 20),

                  TextField(
                    controller:
                        passwordController,
                    focusNode:
                        passwordFocus,
                    obscureText: true,
                    textInputAction:
                        TextInputAction.done,
                    onSubmitted: (_) {
                      login();
                    },
                    decoration:
                        const InputDecoration(
                      hintText:
                          "Password",
                    ),
                  ),

                  const SizedBox(
                      height: 30),

                  SizedBox(
                    width:
                        double.infinity,
                    height: 50,
                    child:
                        ElevatedButton(
                      onPressed: login,
                      child: const Text(
                        "LOGIN",
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}