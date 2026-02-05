from django.http import JsonResponse
from django.shortcuts import render
from core.auth import api_login_required

TEAM_NAME = "team7"

@api_login_required
def ping(request):
    return JsonResponse({"team": TEAM_NAME, "ok": True})

def base(request):
    return render(request, f"{TEAM_NAME}/index.html")

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from core.auth import api_login_required
from .models import Question, Evaluation, DetailedScore
from .services import WritingEvaluator

@csrf_exempt
@require_POST
@api_login_required
def submit_writing(request):
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        question_id = data.get('question_id')
        
        if not text or not question_id:
            return JsonResponse({'error': 'Missing text or question_id'}, status=400)

        try:
            question = Question.objects.get(question_id=question_id)
        except Question.DoesNotExist:
            return JsonResponse({'error': 'Invalid Question ID'}, status=404)

        evaluator = WritingEvaluator()
        
        # 1. Validation (Mode aware)
        is_valid, msg = evaluator.validate_length(text, question.mode)
        if not is_valid:
            return JsonResponse({'error': msg}, status=400)

        # 2. AI Analysis
        ai_result = evaluator.analyze(text, question)
        
        if not ai_result:
            return JsonResponse({'error': 'AI Service unavailable'}, status=503)

        # 3. Parse Psychometric Data
        scores = ai_result.get('scores', {})
        feedback = ai_result.get('feedback_persian', {})
        dimensions = ai_result.get('dimensions', [])

        # 4. Save Evaluation
        evaluation = Evaluation.objects.create(
            user_id=request.user.id,
            question=question,
            submitted_text=text,
            overall_score=scores.get('band_score', 0),
            traditional_score=scores.get('traditional_scale', 0),
            cefr_level=scores.get('cefr_alignment', ''),
            ai_feedback=feedback.get('summary', ''),
            grammar_tips=feedback.get('grammar_tips', '')
        )

        # 5. Save Detailed Scores (Dimensions)
        detailed_data = []
        for dim in dimensions:
            ds = DetailedScore.objects.create(
                evaluation=evaluation,
                criterion=dim.get('name'),
                score_value=dim.get('score'),
                comment=dim.get('comment')
            )
            detailed_data.append({
                'criterion': ds.criterion,
                'score': ds.score_value,
                'comment': ds.comment
            })

        # 6. Response
        return JsonResponse({
            'status': 'success',
            'evaluation_id': str(evaluation.evaluation_id),
            'scores': scores,
            'feedback_persian': feedback,
            'detailed_scores': detailed_data
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)