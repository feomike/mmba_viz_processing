#hex_lp {
  line-color:#51973f;
  line-width:0.5;
  polygon-opacity:.75;
  [lp_average > 4]{
	  polygon-fill:#2b8e00;
    }  
  [lp_average > 1][lp_average <= 4]{
	  polygon-fill:#4ea429;
    }
  [lp_average > 0][lp_average <= 1]{
	  polygon-fill:#41db00;
    }  
   [lp_average = 0]{
	  polygon-fill:#92ed6b;
    }   
}
