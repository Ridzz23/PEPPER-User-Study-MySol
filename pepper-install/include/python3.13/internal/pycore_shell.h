#ifndef Py_CORE_SHELL_H
#define Py_CORE_SHELL_H

#define Py_TPFLAGS_SHELL_OBJ (1UL << 28)

#define PyShell_CheckFast(op) \
    (Py_TYPE(op)->tp_flags & Py_TPFLAGS_SHELL_OBJ)

#ifndef Py_BUILD_CORE
#  error "this header requires Py_BUILD_CORE define"
#endif

#include "Python.h"

typedef struct {
    PyObject_HEAD
    PyObject *cmd_parts; 
    int open_for_args;
    PyObject *stdin_path;
} PyShellObject;

typedef struct PyShellState{
    int bash_stdin;
    int bash_stdout;
    pid_t bash_pid;
} PyShellState;

typedef struct {
    int read_fd; 
    int write_fd;  
    PyObject *buffer; 
} PyShell_Pipe;

typedef struct {
    PyObject_HEAD
    PyObject *data;
} PyShellPipeSourceObject;

typedef struct CommandEntry {
    char *command;
    struct CommandEntry *next;
} CommandEntry;

#define TABLE_SIZE 256

static CommandEntry *command_cache[TABLE_SIZE];

extern PyTypeObject PyShell_Type;
extern PyTypeObject _PyShellPipeSource_Type;

#define PyShell_Check(op) Py_IS_TYPE(op, &PyShell_Type)

PyObject* _PyShell_ExecuteCommand(PyObject *cmd_obj);
int is_shell_command(const char *name);

PyObject* convert_python_func_to_shell_input(PyObject *py_str);

#endif /* !Py_CORE_SHELL_H */