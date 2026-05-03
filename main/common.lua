
function get_angle(vector)
  -- ベクトルから角度を求めるやつ
  angle = math.acos(vmath.dot(vector, vmath.vector3(0, 1, 0))/vmath.length(vector))
  return angle
end

function generate_random_vector()
	x = math.random() * 2 - 1
	y = math.random() * 2 - 1
	return vmath.normalize(vmath.vector3(x, y, 0))
end
