#include <iostream>
#include <vector>
#include <climits>
#define VISITED 1
#define UNVISITED 0
#define NO_EDGE 0

int main(void)
{
	int numOfVertices;
	/* (i, j) represent the weight of edge between i and j, 
       and 0 indicates there is no edge between i and j */ 	
	int ** adjacencyMatrix; 
	bool *arrayS;
	int *arrayQ;
	int *arrayU;
	int startingVertex;
	int numOfVisitedVertex = 1;
	std::cout << "Enter no. of vectors: ";
	std::cin >> numOfVertices;
	adjacencyMatrix = new int*[numOfVertices+1];
	for(int i = 0; i <= numOfVertices; i++)
	{
		adjacencyMatrix[i] = new int[numOfVertices+1];
	}
	arrayS = new bool[numOfVertices+1];
	arrayQ = new int[numOfVertices+1];
	arrayU = new int[numOfVertices+1];
	// input adjacencyMatrix
	std::cout << "Enter adjacency matrix: ";
	for(int i = 1; i <= numOfVertices; i++)
	{
		for(int j = 1; j <= numOfVertices; j++)
		{
			std::cin >> adjacencyMatrix[i][j];		
		}
	}
	std::cout << "Enter starting vertex: ";
	std::cin >> startingVertex;
	for(int i = 0; i <= numOfVertices; i++)
	{
		if(i == startingVertex)			
			arrayS[i] = VISITED;
		else
		    arrayS[i] = UNVISITED;
	}
	
	for(int i = 0; i <= numOfVertices; i++)
	{
		if(i == startingVertex)
			arrayU[i] = 0;
		else if(adjacencyMatrix[startingVertex][i] != NO_EDGE)
			arrayU[i] = adjacencyMatrix[startingVertex][i];
		else
			arrayU[i] = INT_MAX;
	}
	for(int i = 0; i <= numOfVertices; i++)
	{
		arrayQ[i] = startingVertex;
	}
	int minAdjacentVertex = startingVertex;
	while(numOfVisitedVertex < numOfVertices)
	{	   
		int minAdjacentVertexPathLength = INT_MAX;
		int j;
		for(j = 1; j <= numOfVertices; j++)
		{			
			if(arrayS[j] == UNVISITED)
			{
				if(minAdjacentVertexPathLength > arrayU[j])
				{
					// find the adjacent vertex with the minimum path.
				    minAdjacentVertexPathLength = arrayU[j]; // u_j
					minAdjacentVertex = j;
				}
			}
		}
		arrayS[minAdjacentVertex] = VISITED;
		for(int i = 1; i <= numOfVertices; i++)
		{
			int weight = adjacencyMatrix[minAdjacentVertex][i];
			if(arrayS[i] == UNVISITED && weight != NO_EDGE) 			    
			{
				int distanceSum = minAdjacentVertexPathLength + weight; 
				if(arrayU[i] > distanceSum)
				{
					arrayU[i] = distanceSum;
					arrayQ[i] = minAdjacentVertex;
				}
			}
		}
		numOfVisitedVertex++;
	}
	std::cout << "The shortest path from vertex "
			  << startingVertex << std::endl;
	for(int i = 1; i <= numOfVertices; i++)
	{
		if(i != startingVertex)
		{
			std::cout << "Vertex " << i << ": distance "
					  << arrayU[i] << " from vertex " << arrayQ[i] << std::end;  
		}
	}
	delete [] arrayU;
	delete [] arrayQ;
	delete [] arrayS;
	for(int i = 0; i < numOfVertices+1; i++)
	{
		delete [] adjacencyMatrix[i];
	}
	delete [] adjacencyMatrix;
	return 0;
}
