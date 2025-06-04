/**
* @file kdtree.cpp
* @brief arquivo de implementação para vertice da arvore k dimensional utilizada no trabalho pratico
* @authors Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
* @date 20250601 arquivo criado
*/

#include"../include/kdtree.hpp"

//========================================================================
// TODO : implementar insercao balanceada (melhoraria bastante o codigo)
// TODO : (opcional) colocar um report subtree menos comparacoes
//========================================================================

/**
 * @brief Insere um novo vertice na subarvore recursivamente
 * 
 * @param cell apontador para vertice corrente
 * @param new_cell apontador para vertice a ser inserido
 * @param depth profundidade para decidir qual coordenada usar na comparacao
 * @return ptr_kdcell_t apontador para o vertice resultande da subarvore apos insercao
 */
ptr_kdcell_t kdtree_t::insert_recursive(ptr_kdcell_t cell, ptr_kdcell_t new_cell, int depth)
{
    if(cell==nullptr)
        return(new_cell);

    int axis=depth%K; //(0=x, 1=y)

    if(axis==0){
        if(new_cell->coordinates.x < cell->coordinates.x)
            cell->left=insert_recursive(cell->left, new_cell, depth+1);
        else
            cell->right=insert_recursive(cell->right, new_cell, depth+1);
    }
    else{
        if(new_cell->coordinates.y < cell->coordinates.y)
            cell->left=insert_recursive(cell->left, new_cell, depth+1);
        else
            cell->right=insert_recursive(cell->right, new_cell, depth+1);
    }
    return(cell);
}
// END insert_recursive()

void kdtree_t::insert(ptr_kdcell_t new_cell)
{
    root=insert_recursive(root,new_cell,0);
}
// END insert()

/**
 * @brief 
 * 
 * @param cell vertice corrente da arvore
 * @param lower limite inferior das coordenadas
 * @param upper limite superior das coordenadas
 * @param depth profundidade determina coordenada da comparacao
 * @param result lista para resultados encontrados passada por referencia
 */
void kdtree_t::orthogonal_search_recursive(ptr_kdcell_t cell, const coordinates_t& lower,
    const coordinates_t& upper, int depth,
    std::vector<ptr_kdcell_t>& result)
{
    if(cell==nullptr)return;

    const coordinates_t& p=cell->coordinates;
    
    if(p.x>lower.x and p.x<=upper.x and p.y>=lower.y and p.y<=upper.y)
        result.push_back(cell);

    int axis=depth%K; //(0=x, 1=y)

    if(axis==0){
        if(lower.x<=p.x)
            orthogonal_search_recursive(cell->left,lower,upper,depth+1,result);
        if(upper.x>=p.x)
            orthogonal_search_recursive(cell->right,lower,upper,depth+1,result);
    }
    else{
        if(lower.y<=p.y)
            orthogonal_search_recursive(cell->left,lower,upper,depth+1,result);
        if(upper.y >= p.y)
            orthogonal_search_recursive(cell->right,lower,upper,depth+1,result);
    }
}
// END orthogonal_search_recursive()

/**
 * @brief Base da busca intervalar ortogonal
 * 
 * @param lower limite inferior das coordenadas
 * @param upper limite superior das coordenadas
 * @return std::vector<ptr_kdcell_t> lista com vertices encontrados na regiao de busca ortogonal
 */
std::vector<ptr_kdcell_t>kdtree_t::orthogonal_search(const coordinates_t& lower,
                                                     const coordinates_t& upper)
{
    std::vector<ptr_kdcell_t>result;
    orthogonal_search_recursive(root,lower,upper,0,result);
    return(result);
}
// END orthogonal_search()