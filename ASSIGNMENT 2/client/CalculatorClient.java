package client;

import java.util.Scanner;

import org.omg.CORBA.ORB;
import org.omg.CosNaming.*;

import calculator_module.Calculator;
import calculator_module.CalculatorHelper;

public class CalculatorClient {

    public static void main(String args[]) {

        try {

            // Initialize ORB
            ORB orb = ORB.init(args, null);

            // Get naming context reference
            org.omg.CORBA.Object objRef =
                    orb.resolve_initial_references("NameService");

            NamingContextExt ncRef =
                    NamingContextExtHelper.narrow(objRef);

            // Resolve object reference
            String name = "Calculator";

            Calculator calculator =
                    CalculatorHelper.narrow(
                            ncRef.resolve_str(name));

            System.out.println("Connected to Calculator Server");

            Scanner sc = new Scanner(System.in);

            int choice;

            do {

                System.out.println("\n===== CALCULATOR MENU =====");
                System.out.println("1. Add");
                System.out.println("2. Subtract");
                System.out.println("3. Multiply");
                System.out.println("4. Divide");
                System.out.println("5. Exit");

                System.out.print("Enter Your Choice: ");
                choice = sc.nextInt();

                // Exit directly
                if (choice == 5) {
                    System.out.println("Exiting Calculator...");
                    break;
                }

                // Validate menu choice
                if (choice < 1 || choice > 5) {
                    System.out.println("Invalid Choice");
                    continue;
                }

                // Ask numbers only after operation selected
                System.out.print("Enter First Number: ");
                int num1 = sc.nextInt();

                System.out.print("Enter Second Number: ");
                int num2 = sc.nextInt();

                int result = 0;

                switch (choice) {

                    case 1:
                        result = calculator.add(num1, num2);
                        System.out.println(
                                "Addition Result = " + result);
                        break;

                    case 2:
                        result = calculator.subtract(num1, num2);
                        System.out.println(
                                "Subtraction Result = " + result);
                        break;

                    case 3:
                        result = calculator.multiply(num1, num2);
                        System.out.println(
                                "Multiplication Result = " + result);
                        break;

                    case 4:

                        if (num2 == 0) {
                            System.out.println(
                                    "Cannot divide by zero");
                        } else {

                            result =
                                    calculator.divide(num1, num2);

                            System.out.println(
                                    "Division Result = " + result);
                        }

                        break;
                }

            } while (true);

            sc.close();

        } catch (Exception e) {

            System.out.println("ERROR : " + e);
            e.printStackTrace(System.out);
        }
    }
}