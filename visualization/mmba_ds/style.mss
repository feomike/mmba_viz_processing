#hex_ds {
  line-color:#51973f;
  line-width:0.5;
  polygon-opacity:.75;
  [ds_average > 2000000]{
	  polygon-fill:#2b8e00;
    }  
  [ds_average > 1500000][ds_average <= 2000000]{
	  polygon-fill:#4ea429;
    }
  [ds_average > 1000000][ds_average <= 1500000]{
	  polygon-fill:#41db00;
    }  
   [ds_average <= 1000000]{
	  polygon-fill:#92ed6b;
    }   
}
