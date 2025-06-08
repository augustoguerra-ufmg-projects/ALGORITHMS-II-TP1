/**
* @file kdcell.hpp
* @brief arquivo de cabeçalho para vertice da arvore k dimensional utilizada no trabalho pratico
* @authors Augusto G.Lima, Cauã M.Pereira, Heitor G.Leite
* @date 20250528 arquivo criado
*/

#ifndef KDCELL_HPP
#define KDCELL_HPP

#include<string>
#include<iostream>

/**
* @brief definindo tipos abstratos de dados auxiliares, a saber
* coordenadas, data e endereço para uma célula da kdtree
*/

class coordinates_t
{
public:
    double x,y;

    coordinates_t(double _x=0.0, double _y=0.0):x(_x),y(_y){}
};

class date_t
{
public:
    unsigned int day;
    unsigned int month;
    unsigned int year;
    // std::string month;

    date_t(unsigned int d=1, unsigned int m=1, unsigned int y=2000):day(d),month(m),year(y){}
};

class address_t
{
public:
    std::string street;
    std::string street_type;
    std::string neighborhood;
    unsigned int number;
    std::string complement;

    address_t(const std::string& st="", const std::string& stt="", const std::string& neig="", unsigned int n=0, const std::string & c=""):
    street(st),street_type(stt),neighborhood(neig),number(n),complement(c){}
};

/*
* @brief vertice da arvore de quadrantes
*/

class kdcell_t
{
    kdcell_t* left;
    kdcell_t* right;
    coordinates_t coordinates;

    /// dados que o vimogueiro pediu para manter
    std::string name;
    std::string fantasy_name;
    bool permit; /// alvará
    date_t start_date;
    address_t address;

    kdcell_t(const coordinates_t& c, const std::string& n, const std::string& fn, bool p, const date_t& d, const address_t& a): 
    left(nullptr), right(nullptr), coordinates(c), name(n), fantasy_name(fn), permit(p), start_date(d), address(a) {}
};

typedef kdcell_t* ptr_kdcell_t;

#endif // KDCELL_HPP