#!/usr/bin/python
##  CSE6140 HW2
##  This assignment requires installation of networkx package if you want to make use of available graph data structures or you can write your own!!
##  Please feel free to modify this code or write your own

import time
import sys

class RunExperiments:
    def read_graph(self, filename):
        with open(filename, 'rb') as gf:
            n, m = [int(l) for l in gf.readline().split()]
            edge_list=[]
            for i in range(m):
                v1,v2,w=[int(l) for l in gf.readline().split()]
                edge_list.append((w,v1,v2))
        return n,m,edge_list
    
    def computeMST(self,n,edge_list):       
        edge_list.sort(key=lambda tup: tup[0])
        
        parent = dict((i,i) for i in range(n))
        rank = dict((i,0) for i in range(n))
        
        def find(vertice):   
            if parent[vertice] == vertice:
                return vertice
            else:
                parent[vertice] = find(parent[vertice])
                return parent[vertice]
        
        def union(find_v1, find_v2):
            
            if rank[find_v1]>rank[find_v2]:
                parent[find_v2]=find_v1
                
            elif rank[find_v1]<rank[find_v2]:
                parent[find_v1]=find_v2
                
            else:    
                parent[find_v2]=find_v1
                rank[find_v1] += 1
                
        minimum_spanning_tree = []
        mst_span=0
        mst_edge_count=0
        
        i=0
        while(mst_edge_count<n-1):
            
            weight, vertice1, vertice2 = edge_list[i]
            i+=1
            find_v1=find(vertice1)
            find_v2=find(vertice2)
            
            if find_v1!= find_v2:  
                #print("if loop running")
                union(find_v1, find_v2)        
                minimum_spanning_tree.append((weight, vertice1, vertice2))
                mst_edge_count+=1
                mst_span+=weight
                
        return mst_span,minimum_spanning_tree
   		
    def recomputeMST(self,u, v, weight,n,minimum_spanning_tree):
        edge_list=minimum_spanning_tree.copy()
        edge_list.append((weight,u,v))    
        new_mst_span,new_minimum_spanning_tree=self.computeMST(n,edge_list)   
        return new_mst_span,new_minimum_spanning_tree
    
    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print ("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        #Construct graph
        
        n,m,edge_list = self.read_graph(graph_file)

        start_MST = time.time() #time in seconds
        MSTweight,minimum_spanning_tree = self.computeMST(n,edge_list) #call MST function to return total weight of MST
        total_time = (time.time() - start_MST) * 1000 #to convert to milliseconds

        #Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time)+'\n')

        #Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                #parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u,v,weight = edge_data[0], edge_data[1], edge_data[2]

                #call recomputeMST function
                start_recompute = time.time()
                new_weight,new_minimum_spanning_tree = self.recomputeMST(u, v, weight,n,minimum_spanning_tree)
                total_recompute = (time.time() - start_recompute) * 1000 # to convert to milliseconds

                # for the next iteration
                minimum_spanning_tree=new_minimum_spanning_tree.copy()
                
                #write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute)+'\n')
                
        output.close()

if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()
