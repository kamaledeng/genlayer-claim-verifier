# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


class ClaimVerifier(gl.Contract):
    claim: str
    source_url: str
    verdict: str
    explanation: str

    def __init__(self):
        self.claim = ""
        self.source_url = ""
        self.verdict = ""
        self.explanation = ""

    @gl.public.write
    def verify_claim(self, claim: str, source_url: str):

        def leader_fn():
            response = gl.nondet.web.get(source_url)
            page = response.body.decode("utf-8")

            # Limit the amount of webpage text sent to the model.
            page = page[:12000]

            prompt = f"""
You are an evidence verification agent.

Claim:
{claim}

Source URL:
{source_url}

Source content:
{page}

Determine whether the source content actually supports the claim.

Return JSON with exactly these fields:
{{
    "verdict": "supported" or "not_supported",
    "explanation": "brief explanation based only on the source"
}}

Do not use outside knowledge.
"""

            return gl.nondet.exec_prompt(
                prompt,
                response_format="json"
            )

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            validator_result = leader_fn()

            if not isinstance(validator_result, dict):
                return False

            leader_data = leader_result.calldata

            if not isinstance(leader_data, dict):
                return False

            leader_verdict = leader_data.get("verdict")
            validator_verdict = validator_result.get("verdict")

            # Validators independently inspect the source.
            # Only the actual decision must agree.
            return leader_verdict == validator_verdict

        result = gl.vm.run_nondet_unsafe(
            leader_fn,
            validator_fn
        )

        if not isinstance(result, dict):
            raise gl.UserError("Invalid verification result")

        verdict = result.get("verdict")
        explanation = result.get("explanation")

        if verdict not in ["supported", "not_supported"]:
            raise gl.UserError("Invalid verdict")

        self.claim = claim
        self.source_url = source_url
        self.verdict = verdict
        self.explanation = explanation

        return {
            "claim": self.claim,
            "source_url": self.source_url,
            "verdict": self.verdict,
            "explanation": self.explanation
        }

    @gl.public.view
    def get_result(self):
        return {
            "claim": self.claim,
            "source_url": self.source_url,
            "verdict": self.verdict,
            "explanation": self.explanation
        }
