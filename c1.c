#include <stdio.h>                                                   
  1                                                                                                          
  2  int main ( )                                                        
  3  {                                                                 
  4    int m , n , sum = 0 ;                                 
  5    scanf ( " %d %d " , & m , & n ) ;           
  6    for ( int i = n ; m > n ; i ++ ) sum += i * i ;   
  7    print ( " %d " , sum ) ;                               
  8    return 0 ;                                                                      
  9  }  