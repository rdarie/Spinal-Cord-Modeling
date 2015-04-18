function [ out ] = arc_lengths( coords )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

num_points = size(coords, 2);

out = zeros(1,num_points);

for a = 2:num_points
    out(a) = out(a-1) + sqrt(...
        (coords(1,a)-coords(1,a-1)).^2 + ...
        (coords(2,a)-coords(2,a-1)).^2 + ...
        (coords(3,a)-coords(3,a-1)).^2);
end