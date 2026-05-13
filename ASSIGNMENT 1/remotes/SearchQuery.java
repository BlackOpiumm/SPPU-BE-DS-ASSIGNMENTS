package remotes;

import java.rmi.*;
import java.rmi.server.*;

public class SearchQuery extends UnicastRemoteObject
        implements Search {

    public SearchQuery() throws RemoteException {
        super();
    }

    public String login(String username, String password)
            throws RemoteException {

        // User 1
        if (username.equals("shruti")
                && password.equals("1234")) {

            return "Welcome Shruti";
        }

        // User 2
        else if (username.equals("admin")
                && password.equals("admin123")) {

            return "Welcome Admin";
        }

        // User 3
        else if (username.equals("rahul")
                && password.equals("rahul123")) {

            return "Welcome Rahul";
        }

        // User 4
        else if (username.equals("neha")
                && password.equals("neha123")) {

            return "Welcome Neha";
        }

        else {
            return "Invalid username or password";
        }
    }
}