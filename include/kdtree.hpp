/*
* @brief arquivo de cabeçalho para arvore k dimensional utilizada no trabalho pratico
* autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
* histórico : 20250528 arquivo criado
*/

#ifndef KDTREE_H
#define KDTREE_H

#include<bits/stdc++.h>
#include"kdcell.hpp"
using K=2;

class kdtree_t
{
private:
    kdcell_t* root;
    // insert()
    // ortogonal_search()

public:
    kdtree():root(nullptr){}
    //void insert()
    //void search()
};

#endif