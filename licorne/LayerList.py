from licorne import layer

def generate_available_ties(layer_list,incoming_media, substrate):
    ties_nsld_real=[]
    ties_nsld_imaginary=[]
    ties_msld_rho=[]
    ties_msld_theta=[]
    ties_msld_phi=[]
    ties_roughness=[]
    for i,l in enumerate(layer_list):
        if l.nsld_real.vary and l.nsld_real.expr=='':
            ties_nsld_real.append("Layer{0}.nsld_real".format(i))
        if l.nsld_imaginary.vary and l.nsld_imaginary.expr=='':
            ties_nsld_imaginary.append("Layer{0}.nsld_imaginary".format(i))
        if l.msld.rho.vary and l.msld.rho.expr=='':
            ties_msld_rho.append("Layer{0}.msld_rho".format(i))
        if l.msld.theta.vary and l.msld.theta.expr=='':
            ties_msld_theta.append("Layer{0}.msld_theta".format(i))
        if l.msld.phi.vary and l.msld.phi.expr=='':
            ties_msld_phi.append("Layer{0}.msld_phi".format(i))
        if l.roughness.vary and l.roughness.expr=='':
            ties_roughness.append("Layer{0}.roughness".format(i))

    if incoming_media.nsld_real.vary and incoming_media.nsld_real.expr=='':
        ties_nsld_real.append("Incoming_Media.nsld_real")
    if incoming_media.nsld_imaginary.vary and incoming_media.nsld_imaginary.expr=='':
        ties_nsld_imaginary.append("Incoming_Media.nsld_imaginary")
    if incoming_media.msld.rho.vary and incoming_media.msld.rho.expr=='':
        ties_msld_rho.append("Incoming_Media.msld_rho")
    if incoming_media.msld.theta.vary and incoming_media.msld.theta.expr=='':
        ties_msld_theta.append("Incoming_Media.msld_theta")
    if incoming_media.msld.phi.vary and incoming_media.msld.phi.expr=='':
        ties_msld_phi.append("Incoming_Media.msld_phi")
    if incoming_media.roughness.vary and incoming_media.roughness.expr=='':
        ties_roughness.append("Incoming_Media.roughness")

    if substrate.nsld_real.vary and substrate.nsld_real.expr=='':
        ties_nsld_real.append("Substrate.nsld_real")
    if substrate.nsld_imaginary.vary and substrate.nsld_imaginary.expr=='':
        ties_nsld_imaginary.append("Substrate.nsld_imaginary")
    if substrate.msld.rho.vary and substrate.msld.rho.expr=='':
        ties_msld_rho.append("Substrate.msld_rho")
    if substrate.msld.theta.vary and substrate.msld.theta.expr=='':
        ties_msld_theta.append("Substrate.msld_theta")
    if substrate.msld.phi.vary and substrate.msld.phi.expr=='':
        ties_msld_phi.append("Substrate.msld_phi")
    if substrate.roughness.vary and substrate.roughness.expr=='':
        ties_roughness.append("Substrate.roughness")

    return (ties_nsld_real, ties_nsld_imaginary, ties_msld_rho, ties_msld_theta, ties_msld_phi, ties_roughness)


def generate_parameter_lists(layer_list,incoming_media, substrate):
    pass
