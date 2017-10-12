import java.io.*;
import javagently.*;

class GgT{
    public static final String PROMPT = "ggT> ";

    // Funktion ggT nach Euler
    public static int ggT(int a, int b){
	int t;
	
	while (a != 0) {
	    t=a % b;
	    a=b;
	    b=t;
	}
	
	return a;
    }
    
    // Main
    public static void main(String[] argv) throws IOException
    {
	int arg1;
	int arg2;
	int ggT;
	Stream in = new Stream(System.in);
	
	while (true){
	    
	    // Prompt
	    System.out.print(PROMPT);
	    
	    // Eingabe Lesen
	    arg1 = in.readInt();
	    arg2 = in.readInt();
	    // StdInput.readLn();
	    
	    // Pr�fung Eingabe
	    if ((arg1 == 0) || (arg2 == 0)){
		if (arg1==0 && arg2==0){
		    System.exit(0);
		}else{ // Null als ein Argument
		    System.out.println("Fehler! ung�ltiger Wert");
		    continue;
		}
	    }
	    
	    // ggt Ermitteln
	    ggT = ggT(arg1, arg2);
	    
	    // Ergebnis ausgeben
	    System.out.println("ggT("+arg1+", "+arg2+") = "+ggT);
	}
    }
}
