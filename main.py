import building_model as bm

def main():
   results =  bm.run_simulation(num_iters=800)
   results.animate()
 
if __name__ == '__main__':  
	main()