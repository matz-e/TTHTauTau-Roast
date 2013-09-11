// vim: ts=4:sw=4:et:sta

#include <algorithm>

#include "../interface/TLLBranches.h"
#include "../interface/TTLBranches.h"
#include "../interface/Picker.h"

inline double
tau_iso(roast::tll::Branches *b, int idx)
{
    return (*b->TLL_TauHPSbyIsolationMVA2raw)[idx];
}

inline double
ditau_iso(roast::ttl::Branches *b, int idx)
{
    return ((*b->TTL_Tau1HPSbyIsolationMVA2raw)[idx] + 1.) *
        ((*b->TTL_Tau1HPSbyIsolationMVA2raw)[idx] + 1.) +
        ((*b->TTL_Tau2HPSbyIsolationMVA2raw)[idx] + 1.) *
        ((*b->TTL_Tau2HPSbyIsolationMVA2raw)[idx] + 1.);
}

int
roast::ttl::IsoPicker::Pick(roast::Branches *b, const std::vector<int>& idxs)
{
    roast::ttl::Branches *br = dynamic_cast<roast::ttl::Branches*>(b);
    auto idx = std::max_element(idxs.begin(), idxs.end(),
            [&](int a, int b) -> bool { return ditau_iso(br, a) < ditau_iso(br, b); });
    return *idx;
}

int
roast::tll::IsoPicker::Pick(roast::Branches *b, const std::vector<int>& idxs)
{
    roast::tll::Branches *br = dynamic_cast<roast::tll::Branches*>(b);
    auto idx = std::max_element(idxs.begin(), idxs.end(),
            [&](int a, int b) -> bool { return tau_iso(br, a) < tau_iso(br, b); });
    return *idx;
}

ClassImp(roast::ttl::IsoPicker)
