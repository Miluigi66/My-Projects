function windTurbindPowerGetter(resistor, inputSize)
    arguments
        resistor = 100;
        inputSize = 1000;
    end
    close all;
    %a=arduino();
    voltage=zeros(1,inputSize);
    power = zeros(1,inputSize);
    for i=1:inputSize
       % Testing case
       voltageRead = 2*rand(1)+2; %readVoltage(a,'A0');
       voltage(i) = voltageRead;
       power(i) = (voltageRead^2) / resistor;
    end
    % Voltage Graph
    figure();
    plot(voltage);
    title("Voltage Graph");
    ylabel("Voltage (V)");
    % Power Graph
    figure();
    plot(power);
    title("Power Graph (Watts)");
    xlabel("Ristance (" + resistor + " Ohm)");
    ylabel("Voltage^2 (V^2)");
    % Mean of power
    powerMean = mean(voltage.^2/resistor);
    disp("Power: " + powerMean + " Watts.");
    % standard deviation  of voltage
    stdDev = std(voltage);
    disp("Standard Deviation of Voltage: " + stdDev + " V.");
    % standard deviation of power
    powerStdDev = std(voltage.^2 / resistor);
    disp("Standard Deviation of Power: " + powerStdDev + " Watts.");
    disp("");
end
