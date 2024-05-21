import calculate_metrics as cm

#Calculate the Social metric - Rush hour
availability = [cm.availabilityFactor_ICE, cm.availabilityFactor_EV1, cm.availabilityFactor_EV2, cm.availabilityFactor_EV3, cm.availabilityFactor_CNG]
autonomy = [cm.autonomy_ICE, cm.autonomy_EV, cm.autonomy_EV]
cost = [cm.accumulatedCost_ICE[-1], cm.accumulatedCost_EV1[-1], cm.accumulatedCost_EV3[-1], cm.accumulatedCost_CNG[-1]]
incentives = [0 , 9]
emissions = [cm.lifecycleEmissions_ICE, cm.lifecycleEmissions_EV, cm.lifecycleEmissions_CNG]

    data = []
    for i in range(len(availability)):
        availabilityFactor, drivingRangeFactor, costFactor, incentivesFactor, emissionsFactor = [], [], [], [], []
        for j in range(len(availability)):
            availabilityFactor.append(availability[j] / availability[i])
            drivingRangeFactor.append(autonomy[j] / autonomy[i])
            costFactor.append(cost[i] / cost[j])
            incentivesFactor.append(incentives[j] / incentives[i])
            emissionsFactor.append(emissions[i] / emissions[j])
        data.append(availabilityFactor + drivingRangeFactor + costFactor + incentivesFactor + emissionsFactor)




# social = cm.social_metric(cm.generate_alternative_matrix(availability, autonomy, cost, incentives, emissions))

# consumption = [cm.E100km_ICE, cm.E100km_EV]
# cpt = [cm.icr_ICE, cm.icr_EV]
# eco = [cm.emission_ICE, cm.emission_EV]
# emissions = [cm.lifecycleEmissions_ICE, cm.lifecycleEmissions_EV]
# socialCost = [cm.socialCost_ICE, cm.socialCost_EV]

# cm.save_metrics_data(consumption, autonomy, cpt, cost, eco, emissions, socialCost, social, availability)