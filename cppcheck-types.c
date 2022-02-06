#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

/**
 * This files can be used to generated the xml cpp.cfg to inform cppcheck about
 * the used tooclhain type widths and macro values.
 */

#define TYPE(name,sign) \
    __asm__ volatile ("->    <podtype name=\""#name"\" sign=\""#sign"\" size=\"%0\"/>" \
    :: "i"(sizeof(name)));

#define DEF(name) \
    __asm__ volatile ("->    <define name=\""#name"\" value=\"%0\"/>":: "i"(name));

__asm__ (
    "-><?xml version=\"1.0\"?>\n\t"
    "-><def format=\"2\">\n\t"
);

void types() {
    TYPE(signed char,s);
    TYPE(signed short,s);
    TYPE(signed int,s);
    TYPE(signed long int,s);
    TYPE(signed long long int,s);

    TYPE(unsigned char,u);
    TYPE(unsigned short,u);
    TYPE(unsigned int,u);
    TYPE(unsigned long int,u);
    TYPE(unsigned long long int,u);

    TYPE(int8_t,s);
    TYPE(int16_t,s);
    TYPE(int32_t,s);
    TYPE(int64_t,s);
    TYPE(uint8_t,u);
    TYPE(uint16_t,u);
    TYPE(uint32_t,u);
    TYPE(uint64_t,u);

    TYPE(uintptr_t,u);
    TYPE(size_t,u);
}


__asm__ ("-></def>");
