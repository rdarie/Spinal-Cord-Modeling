#include "mujoco2py_functions.hpp"

struct site_functor : Eigen::DenseFunctor<double>
{
	mjModel* _model = new mjModel();
	mjData* _data = new mjData();
	double _target_site_xpos[100];
	int _n_sites;

	std::vector<std::string> _site_name;

	site_functor(mjModel* m, mjData* d, double* tgt, std::vector<std::string> siteNames) : DenseFunctor<double>(6, 24) {

		_model = NULL;
		_model = mj_copyModel(_model, m);

		_data = NULL;
		_data = mj_makeData(_model);

		_site_name = siteNames;
		_n_sites = siteNames.size();

		for (int i = 0; i < 3*_n_sites; i++) {
			_target_site_xpos[i] = tgt[i];
		}
	}

	int operator()(const Eigen::VectorXd &x, Eigen::VectorXd &fvec) const
	{
		double current_site_xpos[100];
		int count = 0;

		for (int i = 0; i < inputs(); i++) {
			_data->qpos[i] = x[i];
			_data->qvel[i] = 0;
			_data->qacc[i] = 0;
		}

		mj_forward(_model,_data);

		for (int i = 0; i < _n_sites; i++) {
			int siteID = mj_name2id(_model, mjOBJ_SITE, _site_name[i].c_str());
			current_site_xpos[count] = _data->site_xpos[3 * siteID + 0];
			count++;
			current_site_xpos[count] = _data->site_xpos[3 * siteID + 1];
			count++;
			current_site_xpos[count] = _data->site_xpos[3 * siteID + 2];
			count++;
		}

		for (int i = 0; i < values(); i++)
		{
			fvec[i] = _target_site_xpos[i] - current_site_xpos[i];
		}
		return 0;
	}

	int df(const Eigen::VectorXd &x, Eigen::MatrixXd &fjac) const
	{
		double jacp[100], jacr[100];
		for (int i = 0; i < _n_sites; i++) {

			int siteID = mj_name2id(_model, mjOBJ_SITE, _site_name[i].c_str());

			for (int i = 0; i < inputs(); i++) {
				_data->qpos[i] = x[i];
				_data->qvel[i] = 0;
				_data->qacc[i] = 0;
			}

			mj_forward(_model, _data);
			mj_jacSite(_model, _data, jacp, jacr, siteID);

			for (int j = 0; j < values()/_n_sites; j++)
			{
				for (int k = 0; k < inputs(); k++) {
					fjac(3*i+j, k) = -jacp[inputs()*j+k];
				}
			}
		}
		return 0;
	}
};

Eigen::VectorXd apply_lm(mjModel* m, mjData* d, double *targ, Eigen::VectorXd x, std::vector<std::string> sites)
{
	int n = 6, info;

	// do the computation
	site_functor functor(m, d, targ, sites);
	Eigen::LevenbergMarquardt<site_functor> lm(functor);

	double factor = 200;
	lm.setFactor(factor);
	//lm.setEpsilon(std::numeric_limits<double>::epsilon());

	//std::cout << "lm.info says: " << lm.info() << std::endl;
	//std::cout << "Starting with a guess of: " << std::endl << x << std::endl;

	info = lm.minimize(x);

	// check return value
	//std::cout << "lm.minimize info was " << info << std::endl;
	//std::cout << "Levenberg Computed" << std::endl << x << std::endl;

	return x;
}

void fitPoseToSites(mjData* d, mjModel*  m, zmq::socket_t *publisher, std::vector<std::string> tendon_names, std::vector<std::string> joint_names, Eigen::VectorXd* solution_pose) {
	// protocol buffer stuff
	mujoco2py::mujoco_msg to_msg;
	mujoco2py::mujoco_msg from_msg;

	mujoco2py::mujoco_msg_mj_act *act_msg = 0;
	mujoco2py::mujoco_msg_mj_joint *joint_msg = 0;
	mujoco2py::mujoco_msg_mj_site *site_msg = 0;

	Eigen::VectorXd actuator_forces(m->nu);
	Eigen::VectorXd joint_forces(m->nv);

	int n = 6;
	Eigen::VectorXd x;

	std::vector<std::string> sites;
	sites.push_back("right_hip");
	sites.push_back("right_knee");
	sites.push_back("right_ankle");
	sites.push_back("right_toe");
	sites.push_back("left_hip");
	sites.push_back("left_knee");
	sites.push_back("left_ankle");
	sites.push_back("left_toe");

	/* the following starting values provide a rough fit. */
	x.setConstant(n, 0);
	for (int j = 0; j < n; j++) {
		x[j] = d->qpos[j];
		//std::cout << "x_i[" << j << "] = " << x[j] << " ";
	}
	//std::cout << std::endl;
	double targ[24];
	//left hip:
	targ[12] = 0.03143;
	targ[13] = 0;
	targ[14] = 0;
	//left knee
	targ[15] = 0.03143;
	targ[16] = 0;
	targ[17] = -0.163;
	//left ankle
	targ[18] = 0.03143;
	targ[19] = 0;
	targ[20] = -0.345;
	//left toe
	targ[21] = 0.03143;
	targ[22] = -0.074;
	targ[23] = -0.345;

	int i = 0;
	for (std::vector<std::string>::iterator it = joint_names.begin(); it < joint_names.end(); it++, i++) {
		int jointID = mj_name2id(m, mjOBJ_JOINT, (*it).c_str());

		joint_msg = to_msg.add_joint();
		(*joint_msg).set_name(*it);
		joint_forces(i) = d->qfrc_inverse[jointID];

		(*joint_msg).set_force(joint_forces(i));
	}

	for (std::vector<std::string>::iterator it = sites.begin(); it < sites.end(); it++) {
		int siteID = mj_name2id(m, mjOBJ_SITE, (*it).c_str());

		site_msg = to_msg.add_site();
		(*site_msg).set_name(*it);
		double y = d->site_xpos[3 * siteID + 1];
		double z = d->site_xpos[3 * siteID + 2];

		(*site_msg).set_y(y);
		(*site_msg).set_z(z);
	}


	Eigen::MatrixXd moment_arm_matrix(m->nu, m->nv);

	for (int i = 0; i < m->nu; i++) {
		for (int j = 0; j < m->nv; j++) {
			moment_arm_matrix(i, j) = d->actuator_moment[m->nv*i + j];
		}
	}

	Eigen::MatrixXd inv_ma_matrix(m->nv, m->nu);
	inv_ma_matrix = moment_arm_matrix.transpose();
	Eigen::JacobiSVD<Eigen::MatrixXd>pinv(inv_ma_matrix);

	actuator_forces = inv_ma_matrix.transpose()*joint_forces;
	//std::cout << "Moment arm matrix: " << std::endl << moment_arm_matrix << std::endl;
	//std::cout << "Actuator Force Vector: " << std::endl << actuator_forces << std::endl;

	i = 0;
	for (std::vector<std::string>::iterator it = tendon_names.begin(); it < tendon_names.end(); it++, i++) {
		int actID = mj_name2id(m, mjOBJ_ACTUATOR, (*it).c_str());

		act_msg = to_msg.add_act();
		(*act_msg).set_name(*it);
		(*act_msg).set_force(actuator_forces(i));
	}

	std::string msg_str;
	to_msg.SerializeToString(&msg_str);

	//  Send message to all subscribers
	zmq::message_t message(msg_str.length());
	memcpy(message.data(), msg_str.c_str(), msg_str.length());
	(*publisher).send(message);

	//  Get the reply.
	zmq::message_t reply;
	(*publisher).recv(&reply);

	from_msg.ParseFromArray(reply.data(), reply.size());

	for (int i = 0; i < from_msg.site_size(); i++) {
		targ[3 * i    ] = from_msg.site(i).x();
		targ[3 * i + 1] = from_msg.site(i).y();
		targ[3 * i + 2] = from_msg.site(i).z();
		/*std::cout << "The reply expects site: " << from_msg.site(i).site_name()
			<< " to be at position <" << from_msg.site(i).x() << ", "
			<< from_msg.site(i).y() << ", " << from_msg.site(i).z() << ">" << std::endl;*/
	}

	(*solution_pose) = apply_lm(m,d,targ,x,sites);
	//std::cout << "solution pose: " << solution_pose.transpose() << std::endl;
	mj_resetData(m, d);
	for (int a = 0; a < m->nq; a++) {
		d->qpos[a] = (*solution_pose)[a];
	}

}

void updateNeuron(mjData* d, mjModel*  m, zmq::socket_t *publisher, std::vector<std::string> tendon_names, std::vector<mjtNum> tendon_length0) {
	// protocol buffer stuff
	mujoco2py::mujoco_msg to_msg;
	mujoco2py::mujoco_msg from_msg;

	mujoco2py::mujoco_msg_mj_tend *tend_msg = 0;

	for (std::vector<std::string>::iterator it = tendon_names.begin(); it < tendon_names.end(); it++) {
		int siteID = mj_name2id(m, mjOBJ_TENDON, (*it).c_str());

		tend_msg = to_msg.add_tend();
		(*tend_msg).set_name(*it);
		(*tend_msg).set_len(d->ten_length[siteID]);
		(*tend_msg).set_len_dot(d->ten_velocity[siteID]);
		//std::cout << "tendon velocity was: " << d->ten_velocity[siteID] << std::endl;
		(*tend_msg).set_len0(tendon_length0[siteID]);
	}

	std::string msg_str;
	to_msg.SerializeToString(&msg_str);

	//  Send message to all subscribers
	zmq::message_t message(msg_str.length());
	memcpy(message.data(), msg_str.c_str(), msg_str.length());
	(*publisher).send(message);

	//  Get the reply.
	zmq::message_t reply;
	(*publisher).recv(&reply);

	from_msg.ParseFromArray(reply.data(), reply.size());
}
