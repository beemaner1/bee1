import java.util.Scanner;

public class gg { 
      
  public static void main (String args[]){
    Scanner in = new Scanner(System.in);
    System.out.print("Input a text: ");
    String st = in.nextLine();
    
    for(int i = 0; i < 9; i++){
      System.out.printf("%d \n", st[i]);
    }
    in.close();

  }
}