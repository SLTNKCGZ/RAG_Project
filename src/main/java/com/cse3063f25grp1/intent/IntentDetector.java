package com.cse3063f25grp1.intent;

import com.cse3063f25grp1.model.Intent;

public interface IntentDetector {
    Intent detect(String question);
}