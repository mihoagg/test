// COS30008, Tutorial 3, 2022

#include "Polynomial.h"
#include <iostream>

Polynomial::Polynomial() {
    fDegree = 0;
    for (size_t i = 0; i <= MAX_DEGREE; i++) {
        fCoeffs[i] = 0.0;
    }
}

Polynomial Polynomial::operator* (const Polynomial& aRHS) const {
    Polynomial A;
    A.fDegree = aRHS.fDegree + fDegree;
    A.fCoeffs[MAX_DEGREE + 1] = {};
    for (size_t i = 0; i <= fDegree; i++) {
        for (size_t j = 0; j <= aRHS.fDegree; j++) {
            A.fCoeffs[i + j] += fCoeffs[i] * aRHS.fCoeffs[j];
        }
    }
    return A;
}

bool Polynomial::operator== (const Polynomial& aRHS) const {
    if (fDegree != aRHS.fDegree) {
        return false;
    }

    for (size_t i = 0; i <= fDegree; i++) {
        if (fCoeffs[i] != aRHS.fCoeffs[i]) {
            return false;
        }
    }

    return true;
};

std::istream& operator>> (std::istream& aIStream, Polynomial& aObject) {
    aIStream >> aObject.fDegree;
    for (int i = aObject.fDegree; i >= 0; --i) {
        aIStream >> aObject.fCoeffs[i];
    }
    return aIStream;
};

std::ostream& operator<<(std::ostream& aOStream, const Polynomial& aObject) {
    bool firstTermPrinted = false;

    for (int i = aObject.fDegree; i >= 0; --i) {
        double coeff = aObject.fCoeffs[i];

        if (coeff != 0) {
            if (firstTermPrinted) {
                aOStream << " + ";
            }
            else {
                firstTermPrinted = true;
            }

            aOStream << coeff << "x^" << i;
        }
    }

    if (!firstTermPrinted) {
        aOStream << "0x^0";  // All zero polynomial
    }

    return aOStream;
}

double Polynomial::operator() (double aX) const {
    double result = 0.0;
    double xPower = 1.0; // x^0 initially
    for (size_t i = 0; i <= fDegree; i++) {
        result += fCoeffs[i] * xPower;
        xPower *= aX; // Increment the power of x
    }
    return result;
}

Polynomial Polynomial::getDerivative() const {
    if (fDegree == 0) {
        // Derivative of constant polynomial is zero polynomial of degree 0 with coeff 0
        Polynomial derivative;
        derivative.fDegree = 0;
        derivative.fCoeffs[0] = 0.0; // zero polynomial
        return derivative;
    }
    Polynomial derivative;
    derivative.fDegree = fDegree - 1; // Degree decreases by 1
    for (size_t i = 1; i <= fDegree; i++) {
        derivative.fCoeffs[i - 1] = fCoeffs[i] * i;
    }
    return derivative;
}

Polynomial Polynomial::getIndefiniteIntegral() const {
    Polynomial integral;
    integral.fDegree = fDegree + 1;
    for (size_t i = 0; i <= fDegree; i++) {
        integral.fCoeffs[i + 1] = fCoeffs[i] / (i + 1);
    }
    integral.fCoeffs[0] = 0.0; // Constant of integration
    return integral;
}

double Polynomial::getDefiniteIntegral(double aXLow, double aXHigh) const {
    Polynomial integral = getIndefiniteIntegral();
    return integral(aXHigh) - integral(aXLow);
}
