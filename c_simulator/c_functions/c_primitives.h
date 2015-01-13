#ifndef C_PRIMITIVE_H
#define C_PRIMITIVE_H

unsigned int int2(const char* str);

int sint2(const char* str);

char* eqpy(const char* str1, const char* str2);

char* extractpy(const char* str1, const char* str2, const char* str3);

char* notpy(const char* str);

char* andpy(const char* str1, const char* str2);

char* orpy(const char* str1, const char* str2);

char* concatpy(const char* str1, const char* str2);

char* bvltpy(const char* str1, const char* str2);

char* bvlepy(const char* str1, const char* str2);

char* bvgtpy(const char* str1, const char* str2);

char* bvgepy(const char* str1, const char* str2);

char* sbvltpy(const char* str1, const char* str2);

char* sbvlepy(const char* str1, const char* str2);

char* sbvgtpy(const char* str1, const char* str2);

char* sbvgepy(const char* str1, const char* str2);

char* bvsxpy(const char* str1, const char* str2);

char* bvpluspy(const char* str1, const char* str2, const char* str3);

char* bvsubpy(const char* str1, const char* str2, const char* str3);

#endif