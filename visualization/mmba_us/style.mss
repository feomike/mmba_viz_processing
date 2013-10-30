#hex_us {
  line-color:#51973f;
  line-width:0.5;
  polygon-opacity:.75;
  [us_average > 1000000]{
	  polygon-fill:#2b8e00;
    }  
  [us_average > 500000][us_average <= 1000000]{
	  polygon-fill:#4ea429;
    }
  [us_average > 250000][us_average <= 500000]{
	  polygon-fill:#41db00;
    }  
   [us_average <= 250000]{
	  polygon-fill:#92ed6b;
    }   
} 
