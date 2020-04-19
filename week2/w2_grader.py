from collections import OrderedDict
import json
import requests
import numpy as np
import warnings


class EMGrader(object):
    def __init__(self):
        self.submission_page = 'https://www.coursera.org/api/' \
                               'onDemandProgrammingScriptSubmissions.v1'
        self.assignment_key = '3ivnq3n_EeexdQ4iFFMrvA'
        self.parts = OrderedDict([
            ('H3evn', 'Task 1 (E-step)'),
            ('uD8jo', 'Task 2 (M-step: mu)'),
            ('zFWgm', 'Task 2 (M-step: sigma)'),
            ('gTUuu', 'Task 2 (M-step: pi)'),
            ('0ZlqN', 'Task 3 (VLB)'),
            ('Olbrx', 'Task 4 (EM)')
        ])
        self.answers = {key: None for key in self.parts}

    @staticmethod
    def ravel_output(output):
        '''
           If student accedentally submitted np.array with one
           element instead of number, this function will submit
           this number instead
        '''
        if isinstance(output, np.ndarray) and output.size == 1:
            output = output.item(0)
        return output

    def submit(self, email, token):
        submission = {
                    "assignmentKey": self.assignment_key,
                    "submitterEmail": email,
                    "secret": token,
                    "parts": {}
                  }
        for part, output in self.answers.items():
            if output is not None:
                submission["parts"][part] = {"output": output}
            else:
                submission["parts"][part] = dict()
        request = requests.post(
            self.submission_page,
            data=json.dumps(submission)
        )
        response = request.json()
        if request.status_code == 201:
            print('Submitted to Coursera platform. '
                  'See results on assignment page!')
        elif u'details' in response and \
                u'learnerMessage' in response[u'details']:
            print(response[u'details'][u'learnerMessage'])
        else:
            print("Unknown response from Coursera:"
                  " {}".format(request.status_code))
            print(response)

    def status(self):
        print("You want to submit these numbers:")
        for part_id, part_name in self.parts.items():
            answer = self.answers[part_id]
            if answer is None:
                answer = '-'*10
            print("Task {}: {}".format(part_name, answer))

    def submit_part(self, part, output):
        self.answers[part] = output
        print("Current answer for task {} is: {}".format(
            self.parts[part], output)
        )

    def submit_e_step(self, output):
        if not np.allclose(np.sum(output, axis=-1), 1):
            warnings.warn('gamma probabilities do not sum to one!')
        self.submit_part('H3evn', str(self.ravel_output(output[9, 1])))

    def submit_m_step(self, pi, mu, sigma):
        if not np.allclose(sigma[0], sigma[0].T):
            warnings.warn(
                'sigma[0, :, :] is not symmetric! '
                'Check that the outer product between vectors is '
                'correct (consider using np.outer).')
        self.submit_part('uD8jo', str(self.ravel_output(mu[1, 1])))
        self.submit_part('zFWgm', str(self.ravel_output(sigma[1, 1, 1])))
        self.submit_part('gTUuu', str(self.ravel_output(pi[1])))

    def submit_VLB(self, loss):
        self.submit_part('0ZlqN', str(self.ravel_output(loss)))

    def submit_EM(self, best_loss):
        if not np.isscalar(best_loss):
            warnings.warn(
                'The loss should be a scalar '
                '(loss from the best restart), not an array.')
        self.submit_part('Olbrx', str(self.ravel_output(best_loss)))
