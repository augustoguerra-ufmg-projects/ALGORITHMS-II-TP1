
/*
* @brief arquivo de cabeçalho para vertice da arvore k dimensional utilizada no trabalho pratico
* autores : Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
* histórico : 20250528 arquivo criado
*/

#ifndef KDTREE_H
#define KDTREE_H

class coordinates_t
{
public:
    double x,y;
    coordinates_t(double _x, double _y):x(_x),y(_y){}
};

class date_t
{
public:
    unsigned int day;
    unsigned int month;
    // string month;
    unsigned int year;
    date_t(unsigned int d, unsigned int m, unsigned int y):day(d),month(m),year(y){}
};

class address_t
{
public:
    string street;
    string street_type;
    string neighborhood;
    unsigned int number;
    string complement;
    address_t(const string& st, cont string& stt, const string& neig, unsigned int n, const string & c):
    street(st),street_type(stt),neighborhood(neig),number(n),complement(c){}
};

class kdcell_t
{
    kdcell_t* left;
    kdcell_t* right;

    /// dados que o vimogueiro pediu para manter
    string name;
    string fantasy_name;
    bool permit; /// alvará
    date_t start_date;
    address_t address;
    kdcell_t():left(nullptr),right(nullptr),permit(false){}
};

#endif