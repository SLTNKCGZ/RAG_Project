package com.cse3063f25grp1.writer;

import java.util.List;

import com.cse3063f25grp1.model.Intent;

public interface QueryWriter {
    List<String> write(String question, Intent intent);
}