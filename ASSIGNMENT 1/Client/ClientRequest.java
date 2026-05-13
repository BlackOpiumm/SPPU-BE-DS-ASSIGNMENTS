package client;

import java.rmi.*;
import java.util.Scanner;

import remotes.Search;

public class ClientRequest {

    public static void main(String[] args) {

        try {

            Scanner sc = new Scanner(System.in);

            System.out.print("Enter Username: ");
            String username = sc.nextLine();

            System.out.print("Enter Password: ");
            String password = sc.nextLine();

            String url = "rmi://localhost:1099/REMOTE_SEARCH";

            Search access = (Search) Naming.lookup(url);

            String result = access.login(username, password);

            System.out.println(result);

            sc.close();

        } catch (Exception e) {
            System.out.println("ClientRequest Exception: " + e.getMessage());
        }
    }
}