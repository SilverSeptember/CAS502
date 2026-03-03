"""Unit tests for the sir_rhs function that's found inn the file cas502/model.py."""

#imports for floating point math and the function we're testing
import math
from cas502.model import sir_rhs




"""
This test checks the SIR model to make sure S I and R's derivatives add up to zero. ... in a basic SIR system there aren't any births, deaths, or migration in/out... people can only move between three compartments: Susceptible, Infected, and Recovered. 
Nobody enters or leaves the population, which means that whenever one compartment loses people, another will always gain the same number. So the total rate of change across all three compartments (dS + dI + dR) should always sum to zero. 
If this test fails, it means the equations in sir_rhs are either creating or destroying people, which would indicate a bug like a wrong sign, a missing term, or a duplicated term.
"""
def test_derivatives_sum_to_zero():
    """SIR is a closed system so dS + dI + dR must equal zero"""
    # Set up an arbitrary scenario: 70% susceptible, 20% infected, 10% recovered
    y = [0.7, 0.2, 0.1]
    #call sir_rhs and assign the three derivatives it returns 
    dS, dI, dR = sir_rhs(y, t=0, beta0=3.0, gamma=1.0)
    """
    dS + dI + dR, 0.0 means this is a closed system so people move between compartments but the total never changes, so the sum of all rates of change must be zero.
    We'll use abs_tol=1e-14 to handle any floating point rounding errors
    """
    assert math.isclose(dS + dI + dR, 0.0, abs_tol=1e-14)




"""
This test checks what happens when there are zero infected people in the population. 
In the SIR model, infection requires contact between susceptible and infected individuals. 
If there are no infected people, no one can transmit the disease and if no one is infected, no one can recover either...so the entire system should be completely still (all three derivatives should be zero. 
This confirms the model works as it should at the edge case where the epidemic either hasn't started yet or has already burned out completely.
"""
def test_no_infection_when_I_is_zero():
    """Without any  infected individuals we should see that nothing changes"""
    #create a situation with zero infected people: 99% susceptible, 0% infected, 1% recovered
    y = [0.99, 0.0, 0.01]
    #then call sir_rhs with a high beta0 to confirm that even strong transmisability can't cause infection when there's nobody around to spread it
    dS, dI, dR = sir_rhs(y, t=0, beta0=15.0, gamma=1.0)
    """
    use == instead of math.isclose because every term in the sir_rhs equations involves multiplying by I. When I is 0.0, those multiplications produce 0.0, not an approximate value but ZERO zero. We don't have a chain of floating point arithmetic to make rounding errors so a strict equality check will work fine.
    """
    assert dS == 0.0
    assert dI == 0.0
    assert dR == 0.0


"""
This test checks what happens when there aren't any susceptible people left in the population. 
In the SIR model new infections depend on the product beta0 * S * I and both susceptibles and infected must be present for transmission to happen.
When S is zero, that product is zero and no new infections can happen, but recovery is still running along. 
Infected people continue to recover at rate gamma, so dI should be negative and dR should be positive. 
This test goes with test_no_infection_when_I_is_zero anf together they confirm that both factors in the infection term matter independently. 
The I=0 test shuts down everything by zeroing out I. This test shuts down only transmission by zeroing out S, while recovery keeps going on and on and on and on.
At least that's the assumption we're making...
"""
def test_no_new_infection_when_S_is_zero():
    """If we don't have any susceptibles then only recovery happens"""
    #create a situation with zero susceptibles, so 0% susceptible, 30% infected, 70% recovered
    y = [0.0, 0.3, 0.7]
    # call sir_rhs with a high beta0 to confirm that even strong transmisability can't generate infections when there's nobody left to infect
    dS, dI, dR = sir_rhs(y, t=0, beta0=15.0, gamma=1.0)
    """
    dS should be zero because the only term that changes S is -beta0 * S * I, and S is zero. 
    We use == here for the same reason as the I=0 test — multiplying by zero gives exact zero.
    But dI and dR are NOT zero. Recovery is still happening:
    dI = -gamma * I (negative, people leaving I) and
    dR = +gamma * I (positive, people arriving in R)
    ...for those we check the direction rather than the exact values
    """
    assert dS == 0.0
    assert dI < 0  # infected are recovering, so I is shrinking
    assert dR > 0  # recovered is growing as people leave I
